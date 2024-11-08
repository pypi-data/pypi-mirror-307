"""Curator: Bespoke Labs Synthetic Data Generation Library."""

import inspect
import json
import logging
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from xxhash import xxh64

from bespokelabs.curator.dataset import Dataset
from bespokelabs.curator.db import MetadataDB
from bespokelabs.curator.prompter.prompt_formatter import PromptFormatter
from bespokelabs.curator.request_processor.generic_request import GenericRequest
from bespokelabs.curator.request_processor.openai_request_processor import (
    OpenAIRequestProcessor,
)

T = TypeVar("T")


class Prompter:
    """Interface for prompting LLMs."""

    def __init__(
        self,
        model_name: str,
        prompt_func: Callable[[Union[Dict[str, Any], BaseModel]], Dict[str, str]],
        parse_func: Optional[
            Callable[
                [Union[Dict[str, Any], BaseModel], Union[Dict[str, Any], BaseModel]], T
            ]
        ] = None,
        response_format: Optional[Type[BaseModel]] = None,
    ):
        """Initialize a Prompter.

        Args:
            model_name (str): The name of the LLM to use
            prompt_func (Callable[[Dict[str, Any]], Dict[str, str]]): A function that takes a single row
                and returns a dict with "system_prompt" and "user_prompt"
            parse_func (Callable[[Dict[str, Any], Any], T]): A function that takes the input row and
                response object and returns the parsed output
            response_format (Optional[Type[BaseModel]]): A Pydantic model specifying the
                response format from the LLM.
        """
        prompt_sig = inspect.signature(prompt_func)
        if len(prompt_sig.parameters) > 1:
            raise ValueError(
                f"prompt_func must take one argument or less, got {len(prompt_sig.parameters)}"
            )

        if parse_func is not None:
            parse_sig = inspect.signature(parse_func)
            if len(parse_sig.parameters) != 2:
                raise ValueError(
                    f"parse_func must take exactly 2 arguments, got {len(parse_sig.parameters)}"
                )

        self.prompt_formatter = PromptFormatter(
            model_name, prompt_func, parse_func, response_format
        )

    def __call__(self, dataset: Optional[Iterable] = None):
        """Run completions on a dataset."""
        return self._completions(dataset)

    def _completions(
        self, dataset: Optional[Iterable] = None, name: Optional[str] = None
    ) -> "Dataset":
        """
        Apply structured completions in parallel to a dataset using specified model and
        prompts.

        Args:
            dataset (Iterable): A dataset consisting of a list of items to apply completions
            prompter (Prompter): A Prompter that contains the logic for formatting each
                item in the dataset
            name (str): Name of the task
            resume (bool): Whether to resume from the previous completions run. If True,
                we use a fingerprint from the input dataset and the prompter to resume
                from a previous run that matches the same fingerprint.

        Returns:
            Iterable: A list of structured outputs from the completions
        """
        if dataset is not None:
            dataset = Dataset.from_iterable(dataset)

        if self is None:
            raise ValueError("Prompter must be provided")

        curator_cache_dir = os.environ.get(
            "CURATOR_CACHE_DIR", os.path.expanduser("~/.cache/curator")
        )

        dataset_hash = _hash_dataset(dataset)
        prompt_func_hash = _get_function_hash(self.prompt_formatter.prompt_func)
        parse_func_hash = _get_function_hash(self.prompt_formatter.parse_func)

        fingerprint_str = "_".join(
            [
                str(dataset_hash),
                str(prompt_func_hash),
                str(parse_func_hash),
                str(self.prompt_formatter.model_name),
                str(
                    self.prompt_formatter.response_format.schema_json()
                    if self.prompt_formatter.response_format
                    else "text"
                ),
            ]
        )

        fingerprint = xxh64(fingerprint_str.encode("utf-8")).hexdigest()

        name = f"{name.replace(' ', '-')}--{fingerprint}" if name else fingerprint
        metadata_db_path = os.path.join(curator_cache_dir, "metadata.db")
        metadata_db = MetadataDB(metadata_db_path)

        # Get the source code of the prompt function
        prompt_func_source = inspect.getsource(self.prompt_formatter.prompt_func)
        if self.prompt_formatter.parse_func is not None:
            parse_func_source = inspect.getsource(self.prompt_formatter.parse_func)
        else:
            parse_func_source = ""

        metadata_dict = {
            "timestamp": datetime.now().isoformat(),
            "dataset_hash": dataset_hash,
            "prompt_func": prompt_func_source,
            "parse_func": parse_func_source,
            "model_name": self.prompt_formatter.model_name,
            "response_format": (
                self.prompt_formatter.response_format.schema_json()
                if self.prompt_formatter.response_format
                else "text"
            ),
            "run_hash": fingerprint,
        }
        metadata_db.store_metadata(metadata_dict)

        request_processor = OpenAIRequestProcessor(self.prompt_formatter)
        return request_processor.run(dataset, f"{curator_cache_dir}/{fingerprint}")


def _hash_chunk(chunks: list) -> list:
    """Hash a chunk of data."""

    def _json_dumps_row(row):
        if isinstance(row, BaseModel):
            row = row.model_dump()
        return json.dumps(row, sort_keys=True)

    chunks = [_json_dumps_row(row) for row in chunks]
    chunk_str = "|||".join(chunks)
    return xxh64(chunk_str).hexdigest()


def _hash_dataset(dataset: Optional[Iterable]):
    """Hash a dataset to a consistent value using parallel processing."""
    start = time.perf_counter_ns()
    if dataset is None:
        return xxh64("").hexdigest()

    # Convert to list and determine chunking parameters
    dataset_list = list(dataset)
    if len(dataset_list) == 0:
        return xxh64("").hexdigest()

    num_cores = 4
    total_size = len(dataset_list)
    chunk_size = math.ceil(total_size / (num_cores * 4))  # 4 chunks per core

    chunks = [
        dataset_list[i : i + chunk_size] for i in range(0, total_size, chunk_size)
    ]

    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        chunk_hash = list(executor.map(_hash_chunk, chunks))
        chunk_hash_str = "|||".join(chunk_hash)
        hash_value = xxh64(chunk_hash_str).hexdigest()

    logging.debug(
        f"Dataset hash time: {(time.perf_counter_ns() - start) / 1e6:.6f} milliseconds"
    )
    return hash_value


def _get_function_hash(func) -> str:
    """Get a hash of a function's source code."""
    if func is None:
        return xxh64("").hexdigest()

    return xxh64(inspect.getsource(func)).hexdigest()

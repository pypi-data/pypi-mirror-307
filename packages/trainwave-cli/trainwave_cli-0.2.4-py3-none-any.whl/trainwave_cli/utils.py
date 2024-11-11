import asyncio
from dataclasses import fields, is_dataclass
from functools import wraps
from typing import TypeVar

import typer

from trainwave_cli.config.config import config


def has_running_event_loop() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        # No running event loop in this thread
        return False


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if has_running_event_loop():
            return f(*args, **kwargs)
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def ensure_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if config.api_key in {"", None}:
            typer.echo(
                "No access token found. Please run `trainwave auth login` to login to your account."
            )
            raise typer.Exit(1)
        return f(*args, **kwargs)

    return wrapper


def truncate_string(s: str, max_len: int) -> str:
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


T = TypeVar("T")


def from_dict(data_class: type[T], data: dict) -> T:
    """Recursively constructs a dataclass from a nested dictionary, skipping unmatched fields."""
    field_names = {f.name for f in fields(data_class)}
    filtered_data = {k: v for k, v in data.items() if k in field_names}

    for key in filtered_data:
        field_type = next(f for f in fields(data_class) if f.name == key).type
        if is_dataclass(field_type):
            filtered_data[key] = from_dict(field_type, filtered_data[key])

    return data_class(**filtered_data)

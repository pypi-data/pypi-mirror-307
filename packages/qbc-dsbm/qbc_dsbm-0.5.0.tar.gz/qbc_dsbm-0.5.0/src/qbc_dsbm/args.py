"""Common argument module."""

# Due to typer usage:
# ruff: noqa: TCH001, TCH003, UP007, FBT001, PLR0913

from __future__ import annotations

from dataclasses import dataclass

import typer


@dataclass
class CommonArgs:
    """Common args and opts."""

    OPT_DEBUG = typer.Option(
        help="Debug mode",
    )

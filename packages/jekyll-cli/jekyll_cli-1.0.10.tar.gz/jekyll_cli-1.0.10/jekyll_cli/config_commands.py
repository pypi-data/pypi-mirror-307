# -*- coding: UTF-8 -*-
from typing import Annotated, Any

from typer import Typer, Argument

from .config import Config
from .prompt import print_config, print
from .utils import convert_literal, check_configuration

app = Typer(
    name='config',
    no_args_is_help=True,
    help='Configuration Subcommands.',
    rich_markup_mode='rich',
)


@app.command(name='list')
def list_config():
    """List all configurations."""
    print_config(Config.to_dict())


@app.command(name='set')
def set_config(
    key: Annotated[str, Argument(help='Configuration key using dot-notation.')],
    value: Annotated[Any, Argument(help='Configuration value.', parser=convert_literal)],
):
    """Set a configuration."""
    check_configuration(key, value)
    Config.update(key, value)
    print(f'Configuration "{key}" updated to "{value}" successfully.')


@app.command()
def reset():
    """Reset default configuration."""
    Config.reset()
    print(f'[green]Reset default configuration successfully.')

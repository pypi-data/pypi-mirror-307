# -*- coding: UTF-8 -*-
from pathlib import Path
from typing import List, Any, Dict

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from rich.console import Console
from rich.table import Table

__console = Console()
print = __console.print
rule = __console.rule


def print_table(items: List[Any], **table_config):
    if not items:
        return
    table = Table(**table_config)
    table.add_column()

    if len(items) == 1:
        table.add_row(f"[green][1][/] {items[0]}")
        print(table)
        return

    table.add_column()
    for i in range(0, len(items), 2):
        item1 = f"[green][{i + 1}][/] {items[i]}"
        item2 = f"[green][{i + 2}][/] {items[i + 1]}" if i + 1 < len(items) else ""
        table.add_row(item1, item2)
    print(table)


def print_info(info: Dict[str, Any], **table_config):
    table = Table(**table_config)
    table.add_column()
    table.add_column()
    for key, value in info.items():
        table.add_row(f'[bold green]{key.capitalize()}', str(value))
    print(table)


def print_config(config: Dict[str, Any], prefix=''):
    for key, value in config.items():
        key = f'{prefix}.{key}' if prefix else key
        if isinstance(value, Dict):
            print_config(value, key)
        else:
            print(f'{key} = {value}')


def select(message, choices: List[Any] | Dict[str, Any]) -> Any:
    match choices:
        case list():
            select_choices = choices
        case dict():
            select_choices = [Choice(name=name, value=value) for name, value in choices.items()]
        case _:
            raise ValueError('choices is not a list or dict.')
    return inquirer.select(
        message=message,
        choices=select_choices,
        vi_mode=True
    ).execute()


def check(message, choices: List[Any] | Dict[str, Any]) -> Any:
    match choices:
        case list():
            select_choices = choices
        case dict():
            select_choices = [Choice(name=name, value=value) for name, value in choices.items()]
        case _:
            raise ValueError('choices is not a list or dict.')
    return inquirer.checkbox(
        message=message,
        choices=select_choices,
        vi_mode=True
    ).execute()


def confirm(message, default=False) -> bool:
    return inquirer.confirm(message, default=default).execute()


class PathValidator(Validator):

    def validate(self, document: Document) -> None:
        if not len(document.text) > 0:
            raise ValidationError(
                message='Input cannot be empty',
                cursor_position=document.cursor_position,
            )
        path = Path(document.text).expanduser()
        if not path.is_dir():
            raise ValidationError(
                message='Input is not a valid path',
                cursor_position=document.cursor_position,
            )
        elif not path.exists():
            raise ValidationError(
                message='Input is not a valid path',
                cursor_position=document.cursor_position,
            )


def input_directory_path(message) -> str:
    return inquirer.filepath(
        message=message,
        vi_mode=True,
        only_directories=True,
        multicolumn_complete=True,
        validate=PathValidator(),
        filter=lambda path: str(Path(path).resolve())
    ).execute()

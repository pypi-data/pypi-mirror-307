# -*- coding: UTF-8 -*-
import ast
import re
from pathlib import Path
from typing import Any, Tuple, Dict, List, Callable

from ruamel.yaml import YAML


def read_markdown(md_file: Path) -> Tuple[Dict[str, Any], str]:
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---\n', maxsplit=2)
    formatter = YAML().load(parts[1]) if parts[1] else {}
    article = parts[2]
    return formatter, article


def write_markdown(md_file: Path, formatter: Dict[str, Any] = None, article: str = ''):
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        if formatter:
            YAML().dump(formatter, f)
        f.write(f'---\n{article}')


def convert_literal(value: str) -> Any:
    try:
        value = ast.literal_eval(value)
        return value
    except Exception:
        return value


def check_configuration(key: str, value: Any):
    match key:
        case 'mode':
            if not isinstance(value, str):
                raise TypeError('value must be a string.')
            if value not in ['single', 'item']:
                raise ValueError('Unexpected value of mode, it can only be "single" or "item".')
        case 'root':
            if not isinstance(value, str):
                raise TypeError('value must be a string.')
            if not Path(value).is_dir():
                raise ValueError('value must be a directory.')
        case _:
            pass


def complete_items(candidates: List[Any]) -> Callable[[str], List[str]]:
    def complete(incomplete: str) -> List[str]:
        return [str(candidate) for candidate in candidates if str(candidate).startswith(incomplete)]


    return complete


def filter_path(mode: str, path: Path) -> bool:
    return path.is_file() if mode == 'single' else path.is_dir()


def split_filename(filename: str) -> Tuple[str, str] | None:
    if not re.match(r'\d{4}-\d{2}-\d{2}-(.+)', filename):
        return None
    parts = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)', filename)
    return parts.group(1), parts.group(2)


def decode_stdout(output):
    try:
        return output.decode('utf-8')
    except UnicodeDecodeError:
        return output.decode('gbk')

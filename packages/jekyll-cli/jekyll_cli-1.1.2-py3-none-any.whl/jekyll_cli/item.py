# -*- coding: UTF-8 -*-
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Literal

from .config import Config
from .enums import BlogType
from .utils import read_markdown, write_markdown, split_filename


class Item:

    def __init__(self, name: str, type_: BlogType, path: Path | None = None, file_path: Path | None = None):
        self.__root = Config.root
        self.__mode = Config.mode
        assert self.__root is not None and self.__mode in ['single', 'item']
        self.name = name
        self.__type = type_
        self.__parent_dir = self.__root / type_.value
        self.__path = path
        self.__file_path = file_path


    @property
    def type(self):
        return self.__type


    @property
    def path(self) -> Path | None:
        r"""
        Return the pathlib.Path of item

        - 'single' mode: the method returns the entire Path of markdown file.
        - 'item' mode: the method returns the entire Path of the item directory.
        :return: the pathlib.Path object or None
        """
        return self.__path


    @property
    def file_path(self) -> Path | None:
        r"""
        Returns the entire pathlib.Path of item's markdown file.
        :return: the pathlib.Path object or None
        """
        if self.__file_path is not None:
            return self.__file_path

        # in single mode, file_path equals to path
        if self.__mode == 'single':
            self.__file_path = self.path
            return self.__file_path

        # in item mode, path is parent path of file_path
        if not self.path:
            return None

        # find .md file for item mode
        pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}$' if self.type == BlogType.Post else self.name
        matched = [f for f in self.path.iterdir() if re.match(pattern, f.stem) and f.is_file()]
        self.__file_path = matched[0] if len(matched) > 0 else None
        return self.__file_path


    def create(self, title: str = None, class_: list[str] = None, tag: list[str] = None):
        # create item directories
        if self.__mode == 'item':
            item_dir = self.__parent_dir / self.name
            assets_dir = item_dir / 'assets'
            item_dir.mkdir(exist_ok=True)
            assets_dir.mkdir(exist_ok=True)

        # .md file processing
        filename = self.name + '.md'
        if self.type == BlogType.Post:
            filename = f'{time.strftime("%Y-%m-%d")}-{filename}'

        file_path = self.__parent_dir / filename if self.__mode == 'single' else self.__parent_dir / self.name / filename
        formatter = Config.get_formatter(self.__type.name)

        # fill current time
        if self.type == BlogType.Post and not formatter['date']:
            formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        # fill formatter
        if title is not None:
            formatter['title'] = title
        if class_ is not None:
            formatter['categories'] = class_
        if tag is not None:
            formatter['tags'] = tag
        write_markdown(file_path, formatter)

        if self.__mode == 'single':
            self.__path = file_path
            self.__file_path = file_path
        else:
            self.__path = file_path.parent
            self.__file_path = file_path


    def open(self, editor=None):
        if not self.file_path:
            raise ValueError('File path is null.')
        command = ['cmd.exe', '/c', 'start', editor if editor else '', self.file_path]
        subprocess.run(command)


    def remove(self):
        if not self.path:
            raise ValueError('Item path is null.')
        if self.__mode == 'single':
            self.path.unlink()
        else:
            shutil.rmtree(self.path)


    def publish(self):
        if self.type != BlogType.Draft:
            raise ValueError('The item is not a draft.')

        if self.path is None or self.file_path is None:
            raise ValueError('Item path or file path is null.')

        self.__parent_dir, self.__path, dest_file_path = self.__move_item('_posts')

        # rename .md file
        post_filename = f'{time.strftime("%Y-%m-%d")}-{dest_file_path.name}'
        dest_file_path = dest_file_path.rename(dest_file_path.with_name(post_filename))
        self.__file_path = dest_file_path

        # update .md file
        formatter, article = read_markdown(dest_file_path)
        formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        write_markdown(dest_file_path, formatter, article)
        self.__type = BlogType.Post


    def unpublish(self):
        if self.type != BlogType.Post:
            raise ValueError('The item is not a post.')

        if self.path is None or self.file_path is None:
            raise ValueError('Item path or file path is null.')

        self.__parent_dir, self.__path, dest_file_path = self.__move_item('_drafts')

        # rename .md file
        draft_filename = dest_file_path.name.split('-', 3)[3]
        dest_file_path = dest_file_path.rename(dest_file_path.with_name(draft_filename))
        self.__file_path = dest_file_path

        # update .md file
        formatter, article = read_markdown(dest_file_path)
        if 'date' in formatter:
            del formatter['date']
        write_markdown(dest_file_path, formatter, article)
        self.__type = BlogType.Draft


    def info(self) -> Dict[str, Any]:
        formatter, _ = read_markdown(self.file_path)
        infos = {
            'name': self.name,
            'type': self.type.name,
            'item-path': self.path,
            'file-path': self.file_path,
        }
        infos = dict(infos, **formatter)
        return infos


    def rename(self, new_name: str):
        if self.path is None or self.file_path is None:
            raise ValueError('Item path or file path is null.')

        new_stem = f'{split_filename(self.file_path.stem)[0]}-{new_name}' if self.type == BlogType.Post else new_name
        self.__file_path = self.file_path.rename(self.file_path.with_stem(new_stem))

        if self.__mode == 'item':
            self.__path = self.path.rename(self.path.with_name(new_name))
        else:
            self.__path = self.__file_path


    def __move_item(self, dest: Literal['_posts', '_drafts']):
        dest_parent_dir = self.__parent_dir.parent / dest
        dest_path = dest_parent_dir / self.path.relative_to(self.__parent_dir)
        dest_file_path = dest_parent_dir / self.file_path.relative_to(self.__parent_dir)
        shutil.move(self.path, dest_path)
        return dest_parent_dir, dest_path, dest_file_path


    def __str__(self):
        return self.name


    def __iter__(self):
        yield from {
            'name': self.name,
            'type': self.type.name,
            'item-path': str(self.path),
            'file-path': str(self.file_path)
        }.items()

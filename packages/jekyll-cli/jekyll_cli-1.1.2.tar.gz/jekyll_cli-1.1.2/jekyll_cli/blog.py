# -*- coding: UTF-8 -*-
from fnmatch import fnmatch
from typing import List, Dict

from .config import Config
from .enums import BlogType
from .item import Item
from .utils import filter_path, split_filename


class __Blog:

    def __init__(self):
        self.__post_items: Dict[str, Item] | None = None
        self.__draft_items: Dict[str, Item] | None = None
        self.__root = Config.root
        self.__mode = Config.mode


    @property
    def posts(self) -> List[Item]:
        return list(self.__posts_dict.values())


    @property
    def drafts(self) -> List[Item]:
        return list(self.__drafts_dict.values())


    @property
    def articles(self) -> List[Item]:
        return self.posts + self.drafts


    @property
    def __posts_dict(self) -> Dict[str, Item]:
        if self.__post_items is None:
            self.__post_items = self.__initialize_items(BlogType.Post)
        return self.__post_items


    @property
    def __drafts_dict(self) -> Dict[str, Item]:
        if self.__draft_items is None:
            self.__draft_items = self.__initialize_items(BlogType.Draft)
        return self.__draft_items


    def find(self, pattern: str, subset: BlogType | None = None) -> List[Item]:
        match subset:
            case BlogType.Post:
                items = self.__posts_dict
            case BlogType.Draft:
                items = self.__drafts_dict
            case _:
                items = dict(self.__posts_dict, **self.__drafts_dict)

        # precise matching
        item = items.get(pattern)
        if item is not None:
            return [item]

        # fuzzy matching
        return [item for name, item in items.items() if fnmatch(name, f'*{pattern}*')]


    def __initialize_items(self, type_: BlogType) -> Dict[str, Item]:
        if self.__root is None:
            return {}
        parent_dir = self.__root / type_.value
        if not parent_dir.is_dir():
            raise ValueError(f'{parent_dir} is not a directory.')

        items = {}
        for item_path in [f for f in parent_dir.iterdir() if filter_path(self.__mode, f)]:
            name = item_path.stem
            if self.__mode == 'single' and type_ == BlogType.Post:
                name = split_filename(item_path.stem)[1]
            items[name] = Item(name, type_, item_path)
        return items


    def __contains__(self, item: Item) -> bool:
        return item.name in (self.__posts_dict if item.type == BlogType.Post else self.__drafts_dict)


Blog: __Blog = __Blog()

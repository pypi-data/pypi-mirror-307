# -*- coding: UTF-8 -*-
from pathlib import Path
from typing import Dict, Any

from omegaconf import OmegaConf as OC


class __Config:
    __DEFAULT_CONFIG__ = {
        'root': None,
        'mode': 'single',
        'generate': {
            'draft': False,
            'port': 4000
        },
        'default': {
            'editor': None,
            'draft': {
                'layout': 'post',
                'title': None,
                'categories': [],
                'tags': []
            },
            'post': {
                'layout': 'post',
                'title': None,
                'categories': [],
                'tags': [],
                'date': None
            }
        }
    }

    __DEPLOY_CONFIG__ = {
        'steps': [
            {'name': None, 'command': None},
            {'name': None, 'command': None},
        ]
    }


    def __init__(self):
        app_home = Path().home() / '.jekyll-cli'
        self.__root: Path | None = None
        self.__mode: str | None = None
        self.config_path = app_home / 'config.yml'
        self.deploy_path = None

        # create app home
        app_home.mkdir(exist_ok=True)

        if not self.config_path.exists():
            # create config.yml
            self.__config = OC.create(self.__DEFAULT_CONFIG__)
            OC.save(self.__config, self.config_path)
        else:
            # read config
            self.__config = OC.load(self.config_path)

        if self.root is not None:
            self.deploy_path = self.root / 'jekyll-deploy.yml'
            if not self.deploy_path.exists():
                self.__deploy_config = OC.create(self.__DEPLOY_CONFIG__)
                OC.save(self.__deploy_config, self.deploy_path)
            else:
                self.__deploy_config = OC.load(self.deploy_path)


    @property
    def root(self) -> Path | None:
        if self.__root is not None:
            return self.__root

        root: str | None = OC.select(self.__config, 'root')
        if not root:
            return None
        root: Path = Path(root)
        if not root.is_dir():
            raise ValueError('Key "root" is not a directory.')
        self.__root = root
        return self.__root


    @property
    def mode(self) -> str:
        if self.__mode is not None:
            return self.__mode

        mode: str = OC.select(self.__config, 'mode', default='single')
        if mode not in ['single', 'item']:
            raise ValueError('Unexpected value of mode.')
        self.__mode = mode
        return self.__mode


    def get_formatter(self, type_: str) -> Dict[str, Any]:
        formatter = self.select(f'default.{type_.lower()}', default={})
        return OC.to_container(formatter, resolve=True)


    def select(self, key: str, default=None) -> Any | None:
        if key.startswith('deploy'):
            key = key.strip('deploy')
            config = self.__deploy_config
        else:
            config = self.__config
        return OC.select(config, key, default=default)


    def update(self, key, value):
        OC.update(self.__config, key, value, merge=False)
        if key == 'root':
            self.__root = value
        elif key == 'mode':
            self.__mode = value
        OC.save(self.__config, self.config_path)


    def reset(self):
        self.__config = OC.create(self.__DEFAULT_CONFIG__)
        OC.save(self.__config, self.config_path)


    def init(self, root, mode, deploy):
        self.__config = OC.unsafe_merge(self.__config, {'root': root, 'mode': mode})
        OC.save(self.__config, self.config_path)

        if deploy:
            self.deploy_path = self.root / 'jekyll-deploy.yml'
            self.__deploy_config = OC.create(self.__DEPLOY_CONFIG__)
            OC.save(self.__deploy_config, self.deploy_path)


    def to_dict(self) -> Dict[str, Any]:
        return OC.to_container(self.__config, resolve=True)


    def __str__(self):
        return OC.to_yaml(self.__config)


Config: __Config = __Config()

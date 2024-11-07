import json
import os
import os.path as osp
import re
import sys


class MapperOption:
    def __init__(self,
                 path_white_list=None,
                 path_black_list=None,
                 name_white_list=None,
                 name_black_list=None,
                 services=None):
        self.options = {
            'path_white_list': path_white_list if path_white_list else [],
            'path_black_list': path_black_list if path_black_list else [],
            'name_white_list': name_white_list if name_white_list else [],
            'name_black_list': name_black_list if name_black_list else [],
            'services': services if services else {},
        }


class BaseEndpointMapper:
    @staticmethod
    def config() -> MapperOption:
        cfg_name = 'emapcfg.json'
        cfg_path = None

        for p in sys.path:
            path = f"{p}/{cfg_name}"
            if osp.exists(path):
                cfg_path = path
                break

        if cfg_path:
            with open(cfg_path, "r") as fp:
                obj = json.load(fp)

            services = obj.get('services')
            if services:
                for key, service in services.items():
                    if service.startswith('$'):
                        env_name = re.search(r"\$\{(.*)}", service).group(1)
                        services[key] = os.environ.get(env_name, None)

            return MapperOption(
                path_white_list=obj.get('path_white_list'),
                path_black_list=obj.get('path_black_list'),
                name_white_list=obj.get('name_white_list'),
                name_black_list=obj.get('name_black_list'),
                services=obj.get('services')
            )
        else:
            return MapperOption()

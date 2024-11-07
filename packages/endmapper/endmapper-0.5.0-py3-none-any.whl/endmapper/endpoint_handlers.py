import json
import logging
import re

import requests


class BaseEndpointHandler:
    def __init__(self, **kwargs):
        self.result = {}
        self.path_white_list = kwargs.get('path_white_list', [])
        self.path_black_list = kwargs.get('path_black_list', [])
        self.name_white_list = kwargs.get('name_white_list', [])
        self.name_black_list = kwargs.get('name_black_list', [])
        self.services = kwargs.get('services', {})
        self.debug = kwargs.get('debug', False)

        if any(w_point in self.path_black_list for w_point in self.path_white_list):
            raise Exception('Black and white path lists cannot have the same values')
        if any(w_point in self.name_black_list for w_point in self.name_white_list):
            raise Exception('Black and white name lists cannot have the same values')

        self.start()

    def start(self):
        pass

    def is_service(self, name, path) -> bool:
        if name in self.services.keys():

            if self.services[name] is None:
                self.result[name] = None
                return True

            try:
                response = requests.get(f'{self.services[name]}api/endpoints/')
                if response.status_code != 200:
                    self.result[name] = None
                    return True

                obj = json.loads(response.content)
                if '<path:path>' in path:
                    path = re.sub('<path:path>/?', '', path)

                for key, value in obj.items():
                    result_path = path + value
                    result_path = result_path.replace('//', '/')
                    self.result[key] = result_path

            except Exception as e:
                logging.error('Service endpoins not found: {}'.format(e))
                self.result[name] = None

            return True
        return False

    def endpoint_valid(self, name, path) -> bool:
        if len(self.name_white_list) > 0 and not any(point in name for point in self.name_white_list):
            return False
        elif len(self.name_black_list) > 0 and any(point in name for point in self.name_black_list):
            return False
        elif len(self.path_white_list) > 0 and not any(point in path for point in self.path_white_list):
            return False
        elif len(self.path_black_list) > 0 and any(point in path for point in self.path_black_list):
            return False

        return True


class DjangoEndpointHandler(BaseEndpointHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        from django.urls import get_resolver

        urlpattern = get_resolver().url_patterns

        for i, item in enumerate(urlpattern):
            urls_list = self.get_urls(item)
            if not urls_list:
                continue

            for key, value in urls_list.items():
                self.result[key] = self.serialize(value)

    def get_urls(self, item, parent_url=''):
        result = {}

        endpoint = str(item.pattern)

        if hasattr(item, 'url_patterns'):
            for pattern in item.url_patterns:
                urls_list = self.get_urls(pattern, parent_url + endpoint)
                if not urls_list:
                    continue

                for key, value in urls_list.items():
                    if value is None:
                        del result[key]
                    else:
                        result[key] = value
        else:   
            while True:
                path = parent_url + endpoint

                if not item.name:
                    if self.debug:
                        print(f'No url patterns found for {path}')
                    break

                if self.is_service(item.name, path):
                    break

                if not self.endpoint_valid(item.name, path):
                    break

                result[item.name] = path
                break

        return result

    @staticmethod
    def serialize(path):
        matches = re.findall(r'<(.*?)>', path)

        for match in matches:
            name = match.split(':')[1]
            path = path.replace(f"<{match}>", '{' + f"{name}" + '}')

        return path


class FastAPIEndpointHandler(BaseEndpointHandler):
    def __init__(self, fastapi_app,  **kwargs):
        super().__init__(**kwargs)
        self.get_urls(fastapi_app.routes)

    def get_urls(self, routes):
        for route in routes:
            name = getattr(route, 'name')
            if not name:
                continue

            while True:
                path = getattr(route, 'path')

                if self.is_service(name, path):
                    break

                if not self.endpoint_valid(name, path):
                    break

                self.result[name] = path
                break

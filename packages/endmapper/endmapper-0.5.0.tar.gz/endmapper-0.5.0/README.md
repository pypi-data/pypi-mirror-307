# Endmapper

Endmapper is a library for mapping endpoints.

## Installation

```bash
pip install endmapper
```

## Config file "cmapcfg.json"

```yaml
{
  //This keywords must be in path
  "path_white_list": [],
  //This keywords could not be in path
  "path_black_list": [],
  //This keywords must be in endpoint name 
  "name_white_list": [],
  //This keywords could not be in endpoint name
  "name_black_list": [],
  //Services use with proxy endpoints
  //Service what you want to connect must use endmapper too
  "services": {
    "endpoint_name": "hostname or ip"
  }
  
  //You can use fields from .env
  "services": {
    "endpoint_name": "${ENV_FIELD}"
  }
  //Use debug mode is you need
  "debug": true,
}
```

## How to use with django/drf

- add new path to main project urls
```python
from django.urls import path, include

urlpatterns = [
    # another paths
    path('', include('endmapper.urls'))
]
```
WARNING: all paths what you want to add to endmapper must have "name" 

## How to use with fastAPI

```python
from fastapi import FastAPI
from endmapper.mappers.fastapi_mapper import connect_app

from lib_1 import  some_router_1
from lib_2 import  some_router_2

app = FastAPI()

app.include_router(some_router_1)
app.include_router(some_router_2)

connect_app(app)
```
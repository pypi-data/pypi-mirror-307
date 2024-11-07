from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from endmapper import endpoint_handlers
from endmapper.mappers.base_mapper import BaseEndpointMapper


router = APIRouter()
main_app = None


def connect_app(app: FastAPI):
    global main_app
    main_app = app
    main_app.include_router(router)


@router.get('/api/endpoints/')
def get_endpoints():
    global main_app
    """
    ATTENTION: include "router" to main FastAPI app

    This will add new endpoint "api/endpoints/" to your project
    """
    if main_app is None:
        return JSONResponse({"error": "FastAPI app not connected"}, status_code=401)

    config = BaseEndpointMapper.config()
    result = endpoint_handlers.FastAPIEndpointHandler(fastapi_app=main_app, **config.options).result

    if 'get_endpoints' in result:
        del result['get_endpoints']

    return JSONResponse(result, status_code=200)

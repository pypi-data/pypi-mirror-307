from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from endmapper.mappers.base_mapper import BaseEndpointMapper
from endmapper import endpoint_handlers


class DjangoEndpointMapper(APIView):
    """
    ATTENTION: add "path("", include("endmapper.urls"))" to main urls

    This will add new endpoint "api/endpoints/" to your project
    """
    @staticmethod
    def get(request):
        config = BaseEndpointMapper.config()
        result = endpoint_handlers.DjangoEndpointHandler(**config.options).result
        return Response(result, status=status.HTTP_200_OK)


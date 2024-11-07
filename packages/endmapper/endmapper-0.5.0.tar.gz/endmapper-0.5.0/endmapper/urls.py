from django.urls import path
from endmapper.mappers import django_mapper

urlpatterns = [
    path('api/endpoints/', django_mapper.DjangoEndpointMapper.as_view())
]
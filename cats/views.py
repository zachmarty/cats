from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from cats.serializers import CatSerializer

# Create your views here.
class CatViewSet(ModelViewSet):
    serializer_class = CatSerializer
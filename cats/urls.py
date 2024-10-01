from django.urls import path

from cats.apps import CatsConfig
from rest_framework.routers import DefaultRouter

from cats.views import BreedListView, CatViewSet

app_name = CatsConfig.name

router = DefaultRouter()
router.register(r'cat', CatViewSet, basename='cat')

urlpatterns = [
    path("breed", BreedListView.as_view(), name="breed"),
] + router.urls

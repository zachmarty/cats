from django.urls import path

from cats.apps import CatsConfig
from rest_framework.routers import DefaultRouter

from cats.views import BreedListView, CatViewSet, RateView

app_name = CatsConfig.name

router = DefaultRouter()
router.register(r'cat', CatViewSet, basename='cat')

urlpatterns = [
    path("breed", BreedListView.as_view(), name="breed"),
    path("rate/<int:cat_id>", RateView.as_view(), name="rate")
] + router.urls

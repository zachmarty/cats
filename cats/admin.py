from django.contrib import admin

from cats.models import Breed, Cat, Rate


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "breed", "color", "age")
    list_filter = (
        "breed",
        "age",
        "color",
    )
    search_fields = ("id", "name")


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent_breed")
    list_filter = ("breed",)
    search_fields = ("id", "name")


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("cat", "user", "value")
    list_filter = ("cat",)
    search_fields = ("cat",)

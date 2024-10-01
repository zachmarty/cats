from rest_framework import serializers
from cats.models import Breed, Cat


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ["name", "color", "age", "breed", "description"]


class BreedSerializer(serializers.ModelSerializer):

    cats = CatSerializer(source="cat_set", many=True, read_only=True)

    class Meta:
        model = Breed
        fields = [
            "name",
        ]

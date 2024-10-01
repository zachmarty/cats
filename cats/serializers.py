from rest_framework import serializers
from cats.models import Breed, Cat, Rate


class CatSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Cat
        fields = ["name", "color", "age", "breed", "description", "rating"]

    def get_rating(self, instance):
        if instance.rate_set.all().count():
            return instance.rate_set.filter(positive = True).count() - instance.rate_set.filter(positive = False).count()
        return 0


class BreedSerializer(serializers.ModelSerializer):

    cats = CatSerializer(source="cat_set", many=True, read_only=True)

    class Meta:
        model = Breed
        fields = [
            "name",
            "cats",
        ]


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = [
            "positive",
        ]

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cats.models import Breed, Cat
from cats.permissions import IsUserOrSuper
from cats.serializers import BreedSerializer, CatSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView


# Create your views here.
class BreedListView(ListAPIView):
    serializer_class = BreedSerializer
    queryset = Breed.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


class CatViewSet(ModelViewSet):

    serializer_class = CatSerializer
    queryset = Cat.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get_permissions(self):
        """Получение прав доступа"""
        if self.action == "update" or self.action == "destroy" or self.action == "partial_update":
            self.permission_classes = [IsAuthenticated, IsUserOrSuper]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = Cat.objects.all()
        breed_name = self.request.query_params.get("breed")
        if breed_name is not None:
            breed = Breed.objects.filter(name=breed_name)
            if breed.exists():
                breed = breed.first()
                queryset = queryset.filter(breed=breed)
        serializer = CatSerializer(queryset, many=True, read_only=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        breed = Breed.objects.filter(id=data["breed"])
        if not breed.exists():
            raise ValidationError(f"Breed with id {data['breed']} does not exist")
        breed = breed.first()
        data["breed"] = breed
        data["user"] = request.user
        new_cat = Cat.objects.create(**data)
        new_cat.save()
        instance = CatSerializer(new_cat)
        return Response(instance.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cats.models import Breed, Cat, Rate
from cats.permissions import IsUserOrSuper
from cats.serializers import BreedSerializer, CatSerializer, RateSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListAPIView, GenericAPIView


# Create your views here.
class RateView(GenericAPIView):
    """
    Rate the cat route
    """
    serializer_class = RateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, cat_id):
        cat = Cat.objects.filter(id = cat_id)
        if not cat.exists():
            raise NotFound(f"Cat with id {cat_id} does not exists")
        cat = cat.first()
        user = request.user
        rate = Rate.objects.filter(user = user)
        data = request.data
        if rate.exists():
            rate = rate.first()
            rate.positive = data['positive']
        else:
            rate = Rate.objects.create(user = user, cat = cat, positive = data['positive'])
        rate.save()
        return Response("rated")





class BreedListView(ListAPIView):
    """
    Breed list route
    """
    serializer_class = BreedSerializer
    queryset = Breed.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


class CatViewSet(ModelViewSet):
    """
    CRUD mechanism for cats
    """
    serializer_class = CatSerializer
    queryset = Cat.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get_permissions(self):
        """Получение прав доступа"""
        if (
            self.action == "update"
            or self.action == "destroy"
            or self.action == "partial_update"
        ):
            self.permission_classes = [IsAuthenticated, IsUserOrSuper]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        """Cat list route"""
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
        """Cat create route"""
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = serializer.validated_data
        data["user"] = request.user
        new_cat = Cat.objects.create(**data)
        new_cat.save()
        instance = CatSerializer(new_cat)
        return Response(instance.data)

    def update(self, request, *args, **kwargs):
        """Cat update route"""
        partial = kwargs.pop("partial", False)
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def retrieve(self, request, *args, **kwargs):
        """Cat retrieve route"""
        return super().retrieve(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Cat destroy route"""
        return super().destroy(request, *args, **kwargs)

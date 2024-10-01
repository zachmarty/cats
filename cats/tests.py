from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
import rest_framework.status as status
from cats.models import Breed, Cat
from users.models import User


# Create your tests here.
class CatTestCase(APITestCase):
    def setUp(self) -> None:
        user = {
            "email": "@test.ru",
            "first_name": "test",
            "last_name": "test",
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        }
        self.test_user = User.objects.create(**user)
        self.test_user.set_password("12345678")
        self.client.force_authenticate(user=self.test_user)

    def test_cat_create(self):
        """Тест создания кота"""
        Breed.objects.create(name="test")
        data = {
            "name": "test",
            "description": "description",
            "age": 2,
            "color": "test",
            "breed": 1,
        }
        response = self.client.post(reverse_lazy("cats:cat-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "name": "test",
                "color": "test",
                "age": 2,
                "breed": 1,
                "description": "description",
                "rating": 0,
            },
        )
        self.assertTrue(Cat.objects.all().exists())
        self.client.session.clear()

    def test_cat_delete(self):
        """Тест удаления кота"""
        breed = Breed.objects.create(name="test")
        data = {
            "name": "test",
            "description": "description",
            "age": 2,
            "color": "test",
            "breed": breed,
            "user": self.test_user,
        }
        Cat.objects.create(**data)
        response = self.client.delete(reverse_lazy("cats:cat-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cat.objects.all().exists())

    def test_cat_list(self):
        """Тест отображения списка котов"""
        breed = Breed.objects.create(name="test")
        data = {
            "name": "test",
            "description": "description",
            "age": 2,
            "color": "test",
            "breed": breed,
            "user": self.test_user,
        }
        Cat.objects.create(**data)
        response = self.client.get(reverse_lazy("cats:cat-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "name": "test",
                    "color": "test",
                    "age": 2,
                    "breed": 3,
                    "description": "description",
                    "rating": 0,
                }
            ],
        )

    def test_cat_retrieve(self):
        """Тест отображения одного кота"""
        breed = Breed.objects.create(name="test")
        data = {
            "name": "test",
            "description": "description",
            "age": 2,
            "color": "test",
            "breed": breed,
            "user": self.test_user,
        }
        Cat.objects.create(**data)
        response = self.client.get(reverse_lazy("cats:cat-detail", kwargs={"pk": 4}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "name": "test",
                "color": "test",
                "age": 2,
                "breed": 4,
                "description": "description",
                "rating": 0,
            },
        )

    def test_cat_update(self):
        """Обновление информации о коте"""
        breed = Breed.objects.create(name="test")
        data = {
            "name": "test",
            "description": "description",
            "age": 2,
            "color": "test",
            "breed": breed,
            "user": self.test_user,
        }
        Cat.objects.create(**data)
        data = {
            "name": "test",
            "description": "description",
            "age": 3,
            "color": "test1",
            "breed": 5,
        }
        response = self.client.put(
            reverse_lazy("cats:cat-detail", kwargs={"pk": 5}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "name": "test",
                "color": "test1",
                "age": 3,
                "breed": 5,
                "description": "description",
                "rating": 0,
            },
        )

    def test_cat_update_partial(self):
        """Тест обновления некоторой информации о коте"""
        breed = Breed.objects.create(name="test")
        data = {
            "name": "test",
            "description": "description",
            "age": 2,
            "color": "test",
            "breed": breed,
            "user": self.test_user,
        }
        Cat.objects.create(**data)
        data = {
            "age": 3,
        }
        response = self.client.patch(
            reverse_lazy("cats:cat-detail", kwargs={"pk": 6}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "name": "test",
                "color": "test",
                "age": 3,
                "breed": 6,
                "description": "description",
                "rating": 0,
            },
        )

    

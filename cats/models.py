from django.db import models

from users.models import User


class Breed(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name="Название")
    parent_breed = models.ForeignKey(
        "Breed",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Родительская порода",
    )

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"
        ordering = [
            "name",
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Cat(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name="Имя")
    color = models.CharField(max_length=40, verbose_name="Цвет")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    description = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name="Описание"
    )
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="Порода")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        verbose_name = "Кот"
        verbose_name_plural = "Коты"
        ordering = [
            "name",
            "breed",
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.age} {self.color}"


class Rate(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, verbose_name="Котенок")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    positive = models.BooleanField(
        default=False, verbose_name="Положительный/негативный"
    )

    class Meta:
        verbose_name = "Отметка"
        verbose_name_plural = "Отметки"
        ordering = ["cat", "user"]

    def __str__(self) -> str:
        return f"{self.cat} {self.positive}"

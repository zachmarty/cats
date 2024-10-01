from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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
    value = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        default=1,
        verbose_name="Оценка",
    )

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["cat", "user"]

    def __str__(self) -> str:
        return f"{self.cat} {self.positive}"

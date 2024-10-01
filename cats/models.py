from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=40, unique=True)
    parent_breed = models.ForeignKey(
        "Breed", on_delete=models.CASCADE, blank=True, null=True
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
    name = models.CharField(max_length=40, unique=True)
    color = models.CharField(max_length=40)
    age = models.PositiveIntegerField()
    description = models.TextField(max_length=1000, blank=True, null=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Кот"
        verbose_name_plural = "Коты"
        ordering = [
            "name",
            "breed",
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.age} {self.color}"

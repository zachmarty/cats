from django.db import models

class Breed(models.Model):
    name = models.CharField(max_length=40, unique=True)
    parent_breed = models.ForeignKey("Breed", on_delete=models.CASCADE, blank=True, null=True)

class Cat(models.Model):
    name = models.CharField(max_length=40, unique=True)
    color = models.CharField(max_length=40)
    age = models.PositiveIntegerField()
    description = models.TextField(max_length=1000, blank=True, null=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

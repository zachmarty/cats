# Generated by Django 5.1.1 on 2024-10-01 13:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('parent_breed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cats.breed')),
            ],
            options={
                'verbose_name': 'Порода',
                'verbose_name_plural': 'Породы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('color', models.CharField(max_length=40)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.breed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Кот',
                'verbose_name_plural': 'Коты',
                'ordering': ['name', 'breed'],
            },
        ),
    ]

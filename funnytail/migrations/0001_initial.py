# Generated by Django 5.0.2 on 2024-03-12 08:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import funnytail.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Breed",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="Порода"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Порода",
                "verbose_name_plural": "Породы",
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["name"], name="funnytail_b_name_04a4a5_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="TagPosts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag", models.CharField(db_index=True, max_length=100)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["tag"],
                "indexes": [
                    models.Index(fields=["tag"], name="funnytail_t_tag_5f9c09_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="Cats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Кличка")),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="Slug"),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to=funnytail.models.get_user_path,
                        verbose_name="Фото",
                    ),
                ),
                ("content", models.TextField(blank=True, verbose_name="Текст статьи")),
                (
                    "time_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создание"
                    ),
                ),
                (
                    "time_update",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время обновления"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        choices=[(False, "Черновик"), (True, "Опубликовано")],
                        default=1,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "breed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="posts",
                        to="funnytail.breed",
                        verbose_name="Порода",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="posts",
                        to="funnytail.tagposts",
                        verbose_name="Теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "Кошки",
                "verbose_name_plural": "Кошки",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=80)),
                ("email", models.EmailField(max_length=254)),
                ("body", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="funnytail.cats",
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
                "indexes": [
                    models.Index(
                        fields=["created"], name="funnytail_c_created_f30d37_idx"
                    )
                ],
            },
        ),
        migrations.AddIndex(
            model_name="cats",
            index=models.Index(fields=["title"], name="funnytail_c_title_9c7fc1_idx"),
        ),
    ]

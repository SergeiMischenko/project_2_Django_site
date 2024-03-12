from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


def get_user_path(instance, filename):
    return f"preview/{instance.author}_user/{filename}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cats.Status.PUBLISHED)


class Cats(models.Model):
    class Meta:
        verbose_name = "Кошки"
        verbose_name_plural = "Кошки"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Кличка")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="Slug"
    )
    preview = models.ImageField(
        upload_to=get_user_path,
        blank=True,
        default=None,
        null=True,
        verbose_name="Фото",
    )
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создание")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED,
        verbose_name="Статус",
    )
    breed = models.ForeignKey(
        "Breed", on_delete=models.PROTECT, related_name="posts", verbose_name="Порода"
    )
    tags = models.ManyToManyField(
        "TagPosts", blank=True, related_name="posts", verbose_name="Теги"
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="posts",
        verbose_name="Автор",
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.is_published:
            return reverse("post", kwargs={"post_slug": self.slug})
        return reverse("home")

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.title, 'ru', reversed=True))
    #     super().save(*args, **kwargs)


class Breed(models.Model):
    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    name = models.CharField(max_length=100, db_index=True, verbose_name="Порода")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.slug})


class TagPosts(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["tag"]
        indexes = [
            models.Index(fields=["tag"]),
        ]

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Cats, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Комментарий {self.name} поста {self.post}"

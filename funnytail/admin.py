from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from funnytail.models import Breed, Cats, TagPosts, Comment


@admin.register(Cats)
class CatAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "slug",
        "content",
        "preview",
        "post_preview",
        "breed",
        "tags",
        "is_published",
        "author",
    ]
    readonly_fields = ["post_preview"]
    prepopulated_fields = {"slug": ("title", "breed", "author")}
    filter_horizontal = ["tags"]
    list_display = ("title", "post_preview", "time_create", "is_published", "breed")
    list_display_links = ("title",)
    ordering = ["-time_create", "title"]
    list_editable = ("is_published",)
    list_per_page = 10
    actions = ["set_published", "set_draft"]
    search_fields = ["title", "breed__name"]
    list_filter = ["breed__name", "is_published"]
    save_on_top = True

    @admin.display(description="Изображение", ordering="content")
    def post_preview(self, cats: Cats):
        if cats.preview:
            return mark_safe(f'<img src="{cats.preview.url}" width=50>')
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Cats.Status.PUBLISHED)
        self.message_user(
            request, f"{count} записей снято с публикации.", messages.WARNING
        )

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Cats.Status.DRAFT)
        self.message_user(request, f"Изменено {count} записей.")


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name", "id"]


@admin.register(TagPosts)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "tag")
    list_display_links = ("id", "tag")
    prepopulated_fields = {"slug": ("tag",)}
    ordering = ["tag", "id"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]

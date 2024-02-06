from django.contrib import admin, messages

from funnytail.models import Cats, Breed


@admin.register(Cats)
class CatAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'breed', 'tags', 'is_published']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ('title', 'time_create', 'is_published', 'breed', 'brief_info')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'breed__name']
    list_filter = ['breed__name', 'is_published']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, cats: Cats):
        return f'Описание {len(cats.content)} символов.'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Cats.Status.PUBLISHED)
        self.message_user(request, f'{count} записей снято с публикации.', messages.WARNING)

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Cats.Status.DRAFT)
        self.message_user(request, f'Изменено {count} записей.')


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name', 'id']

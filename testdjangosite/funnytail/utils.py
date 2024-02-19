from django.conf import settings

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


class DataMixin:
    title_page = None
    category_selected = None
    paginate_by = 10
    default_image = settings.DEFAULT_USER_IMAGE
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if self.category_selected is not None:
            self.extra_context['category_selected'] = self.category_selected
        self.extra_context['default_image'] = self.default_image

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['category_selected'] = None
        context.update(kwargs)
        return context

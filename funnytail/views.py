from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from .forms import ContactForm, PostForm
from .models import Cats, TagPosts
from .utils import DataMixin


class CatsHome(DataMixin, ListView):
    template_name = "funnytail/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    category_selected = 0

    def get_queryset(self):
        return Cats.published.all().select_related("breed", "author")


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = PostForm
    template_name = "funnytail/addpage.html"
    title_page = "Форма для добавление статьи"

    def form_valid(self, form):
        cat = form.save(commit=False)
        cat.author = self.request.user
        return super().form_valid(form)


class UpdatePage(LoginRequiredMixin, DataMixin, UpdateView):
    model = Cats
    fields = ["title", "content", "preview", "is_published", "breed", "tags"]
    template_name = "funnytail/addpage.html"
    title_page = "Редактирование поста"


class CatsCategoryList(DataMixin, ListView):
    template_name = "funnytail/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Cats.published.filter(
            breed__slug=self.kwargs["category_slug"]
        ).select_related("breed", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breed = context["posts"][0].breed
        return self.get_mixin_context(
            context, title="Порода - " + breed.name, category_selected=breed.pk
        )


class PostView(DataMixin, DetailView):
    template_name = "funnytail/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Cats.published, slug=self.kwargs[self.slug_url_kwarg])


class CatsTagList(DataMixin, ListView):
    template_name = "funnytail/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Cats.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related(
            "breed", "author"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = TagPosts.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title="Тег - " + tags.tag)


class UserPosts(DataMixin, ListView):
    template_name = "funnytail/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Cats.objects.filter(
            author__username=self.kwargs["user_name"]
        ).select_related("breed", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context, title=f"Статьи пользователя: {self.kwargs['user_name']}"
        )


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "funnytail/contact.html"
    success_url = reverse_lazy("home")
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


def about(request: HttpRequest):
    data = {"title": "О сайте", "default_image": settings.DEFAULT_USER_IMAGE}
    return render(request, "funnytail/about.html", context=data)


def page_not_found(request: HttpRequest, exception: Exception):
    data = {"title": "Ошибка 404, страница не найдена", "body": "Страница не найдена"}
    return render(request, "funnytail/error404.html", context=data)

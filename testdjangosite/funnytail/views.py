from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import PostForm
from .models import Cats, Breed, TagPosts
from .utils import DataMixin


class CatsHome(DataMixin, ListView):
    template_name = 'funnytail/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    category_selected = 0

    def get_queryset(self):
        return Cats.published.all().select_related('breed')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = PostForm
    template_name = 'funnytail/addpage.html'
    title_page = 'Форма для добавление статьи'

    def form_valid(self, form):
        cat = form.save(commit=False)
        cat.author = self.request.user
        return super().form_valid(form)


class UpdatePage(LoginRequiredMixin, DataMixin, UpdateView):
    model = Cats
    fields = ['title', 'content', 'preview', 'is_published', 'breed', 'tags']
    template_name = 'funnytail/addpage.html'
    title_page = 'Редактирование поста'


class CatsCategoryList(DataMixin, ListView):
    template_name = 'funnytail/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Cats.published.filter(breed__slug=self.kwargs['category_slug']).select_related('breed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breed = context['posts'][0].breed
        return self.get_mixin_context(
            context,
            title='Порода - ' + breed.name,
            category_selected=breed.pk
        )


class PostView(DataMixin, DetailView):
    template_name = 'funnytail/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Cats.published, slug=self.kwargs[self.slug_url_kwarg])


class CatsTagList(DataMixin, ListView):
    template_name = 'funnytail/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Cats.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('breed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = TagPosts.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег - ' + tags.tag)


def contact(request: HttpRequest) -> HttpResponse:
    data = {'title': 'Обратная связь'}
    return render(request, 'funnytail/contact.html', context=data)


def about(request: HttpRequest):
    data = {'title': 'О сайте'}
    return render(request, 'funnytail/about.html', context=data)


def page_not_found(request: HttpRequest, exception):
    data = {'title': 'Ошибка 404, страница не найдена', 'body': 'Страница не найдена'}
    return render(request, 'funnytail/error404.html', context=data)

from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from .forms import AddPostForm
from .models import Cats, Breed, TagPosts

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


class CatsHome(ListView):
    template_name = 'funnytail/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'category_selected': 0,
    }

    def get_queryset(self):
        return Cats.published.all().select_related('breed')


class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'funnytail/addpage.html'
    success_url = reverse_lazy('post', post_slug=form_class.base_fields['slug'])
    extra_context = {
        'menu': menu,
        'title': 'Форма для добавление статьи',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CatsCategoryList(ListView):
    template_name = 'funnytail/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Cats.published.filter(breed__slug=self.kwargs['category_slug']).select_related('breed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breed = context['posts'][0].breed
        context['title'] = 'Порода - ' + breed.name
        context['menu'] = menu
        context['category_selected'] = breed.pk
        return context


class PostView(DetailView):
    template_name = 'funnytail/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Cats.published, slug=self.kwargs[self.slug_url_kwarg])


class CatsTagList(ListView):
    template_name = 'funnytail/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Cats.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('breed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = TagPosts.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег - ' + tags.tag
        context['menu'] = menu
        context['category_selected'] = None
        return context


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Обратная связь</h1>")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Авторизация</h1>")


def about(request: HttpRequest):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'funnytail/about.html', context=data)


def page_not_found(request: HttpRequest, exception):
    data = {'title': 'Ошибка 404, страница не найдена', 'body': 'Страница не найдена'}
    return render(request, 'funnytail/error404.html', context=data)

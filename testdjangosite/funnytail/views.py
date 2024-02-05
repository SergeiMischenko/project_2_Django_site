from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cats, Breed, TagPosts

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]

cats_db = [
    {'id': 1, 'name': 'Персидская'},
    {'id': 2, 'name': 'Сиамская'},
    {'id': 3, 'name': 'Сибирская'},
    {'id': 4, 'name': 'Британская короткошерстная'},
    {'id': 5, 'name': 'Русская голубая'},
    {'id': 6, 'name': 'Скоттиш-фолд'},
    {'id': 7, 'name': 'Мейн-кун'},
    {'id': 8, 'name': 'Невская маскарадная'},
    {'id': 9, 'name': 'Ориентальная короткошерстная'},
    {'id': 10, 'name': 'Сфинкс'},
]


def index(request: HttpRequest):
    posts = Cats.published.all()
    data = {'title': 'Главная страница', 'menu': menu, 'posts': posts, 'category_selected': 0, }
    return render(request, 'funnytail/index.html', context=data)


def addpage(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Добавление статьи</h1>")


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Обратная связь</h1>")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Авторизация</h1>")


def about(request: HttpRequest):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'funnytail/about.html', context=data)


def show_categories(request: HttpRequest, category_slug):
    category = get_object_or_404(Breed, slug=category_slug)
    posts = Cats.published.filter(breed_id=category.pk)
    data = {
        'title': f'Порода: {category.name}',
        'menu': menu,
        'posts': posts,
        'category_selected': category.pk,
    }
    return render(request, 'funnytail/index.html', context=data)


def show_post(request: HttpRequest, post_slug):
    post = get_object_or_404(Cats, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'category_selected': post.breed_id,
    }
    return render(request, 'funnytail/post.html', context=data)


def show_tag_postlist(request: HttpRequest, tag_slug):
    tag = get_object_or_404(TagPosts, slug=tag_slug)
    posts = tag.posts.filter(is_published=Cats.Status.PUBLISHED)

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'category_selected': None,
    }
    return render(request, 'funnytail/index.html', context=data)

def page_not_found(request: HttpRequest, exception):
    data = {'title': 'Ошибка 404, страница не найдена', 'body': 'Страница не найдена'}
    return render(request, 'funnytail/error404.html', context=data)

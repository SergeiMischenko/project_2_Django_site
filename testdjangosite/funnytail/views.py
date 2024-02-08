from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPostForm
from .models import Cats, Breed, TagPosts

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request: HttpRequest):
    posts = Cats.published.all().select_related('breed')
    data = {'title': 'Главная страница', 'menu': menu, 'posts': posts, 'category_selected': 0, }
    return render(request, 'funnytail/index.html', context=data)


def addpage(request: HttpRequest):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post', post_slug=form.cleaned_data['slug'])
    else:
        form = AddPostForm()
    data = {
        'menu': menu,
        'title': 'Форма для добавление статьи',
        'form': form
    }
    return render(request, 'funnytail/addpage.html', context=data)


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Обратная связь</h1>")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Авторизация</h1>")


def about(request: HttpRequest):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'funnytail/about.html', context=data)


def show_categories(request: HttpRequest, category_slug):
    category = get_object_or_404(Breed, slug=category_slug)
    posts = Cats.published.filter(breed_id=category.pk).select_related('breed')
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
    posts = tag.posts.filter(is_published=Cats.Status.PUBLISHED).select_related('breed')

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

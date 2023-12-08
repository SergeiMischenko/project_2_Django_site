from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    data = {'title': 'Главная страница', 'menu': menu}
    return render(request, 'funnytail/index.html', context=data)


def addpage(request):
    return HttpResponse("<h1>Добавление статьи</h1>")


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


def login(request):
    return HttpResponse("<h1>Авторизация</h1>")


def about(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'funnytail/about.html', context=data)


def categories(request, category_id):
    if category_id > 5:
        return redirect('category_id', 1, permanent=True)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {category_id}</p>")


def page_not_found(request, exception):
    data = {'title': 'Ошибка 404, страница не найдена', 'body': 'Страница не найдена'}
    return render(request, 'funnytail/error404.html', context=data)

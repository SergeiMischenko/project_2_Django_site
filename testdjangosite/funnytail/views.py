from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect


def index(request) -> HttpResponse:
    return render(request, 'funnytail/index.html')


def categories(request, category_id) -> HttpResponse:
    if category_id > 5:
        return redirect('category_id', 1, permanent=True)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {category_id}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

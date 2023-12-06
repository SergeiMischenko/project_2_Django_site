from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'funnytail/index.html')


def about(request):
    return render(request, 'funnytail/about.html')


def categories(request, category_id):
    if category_id > 5:
        return redirect('category_id', 1, permanent=True)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {category_id}</p>")


def page_not_found(request, exception):
    return render(request, 'funnytail/error404.html')

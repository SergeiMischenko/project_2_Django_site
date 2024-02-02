from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cats

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

data_db = [
    {'id': 1, 'title': 'Муся',
     'content': '''Эта кошка - воплощение нежности и умиротворенности. Ее характер не отличается 
     невероятным спокойствием особенно в отношении еды, словно она несет в себе частичку тишины и уюта. Ласковая и 
     преданная, она обладает невероятным терпением, всегда готова быть рядом, подарив своё теплое мурчащее компаньонство.
     Эта кошка легко устраивает своё уютное логово, где правит атмосфера умиротворения. Ее глаза, полные нежности, 
     отражают внутренний мир, полный ласки и покоя. В ее прикосновениях скрыта магия, способная зажечь свет в сердце 
     каждого, кто ей откроет свою душу.''', 'preview': '/муся.jpg', 'is_published': True},
    {'id': 2, 'title': 'Белка',
     'content': '''Эта кошка – вихрь радости и бесконечной энергии. Стремительная, словно игривый ветер, она наполняет 
     пространство своим беспокойным жизненным настроением. Всегда в движении, она превращает обыденные моменты в 
     захватывающие игры, прыжки и ловкость в ее арсенале. С ее неудержимой энергией, она обладает чарующей способностью 
     развлекать окружающих. Любопытство исследователя дополняют ее непосредственностью – она находит веселье в каждом 
     уголке дома и заставляет улыбаться своим шаловливым поведением. Ее игривый характер – настоящий источник радости и 
     веселья.''', 'preview': '/белка.jpg', 'is_published': True},
]


def index(request: HttpRequest):
    posts = Cats.published.all()
    data = {'title': 'Главная страница', 'menu': menu, 'posts': posts, 'category_selected': 0,}
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


def show_categories(request: HttpRequest, category_id):
    title = cats_db[category_id-1]['name'] + ' | FunnyTail'
    data = {'title': title, 'menu': menu, 'posts': data_db, 'category_selected': category_id,}
    return render(request, 'funnytail/index.html', context=data)


def show_post(request: HttpRequest, post_slug):
    post = get_object_or_404(Cats, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'category_selected': 0,
    }
    return render(request, 'funnytail/post.html', context=data)


def page_not_found(request: HttpRequest, exception):
    data = {'title': 'Ошибка 404, страница не найдена', 'body': 'Страница не найдена'}
    return render(request, 'funnytail/error404.html', context=data)

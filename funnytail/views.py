from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from .forms import ContactForm, PostForm, SearchForm, CommentForm
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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Cats, id=post_id, is_published=Cats.Status.PUBLISHED)
    title = "Добавить новый комментарий"
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "funnytail/comment.html",
        {"post": post, "title": title, "form": form, "comment": comment},
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector(
                "title", weight="A", config="russian"
            ) + SearchVector("content", weight="B", config="russian")
            search_query = SearchQuery(query, config="russian")
            results = (
                Cats.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gte=0.3)
                .order_by("-rank")
            )
    return render(
        request,
        "funnytail/search.html",
        {"title": "Поиск", "form": form, "query": query, "results": results, "default_image": settings.DEFAULT_USER_IMAGE},
    )


def about(request: HttpRequest):
    data = {"title": "О сайте", "default_image": settings.DEFAULT_USER_IMAGE}
    return render(request, "funnytail/about.html", context=data)


def page_not_found(request: HttpRequest, exception: Exception):
    data = {"title": "Ошибка 404, страница не найдена", "body": "Страница не найдена"}
    return render(request, "funnytail/error404.html", context=data)

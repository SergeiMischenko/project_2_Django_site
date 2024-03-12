from django.urls import path

from . import views

urlpatterns = [
    path("", views.CatsHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("post/<slug:post_slug>/", views.PostView.as_view(), name="post"),
    path("posts/<slug:user_name>/", views.UserPosts.as_view(), name="user_posts"),
    path(
        "category/<slug:category_slug>/",
        views.CatsCategoryList.as_view(),
        name="category",
    ),
    path("tag/<slug:tag_slug>/", views.CatsTagList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("search/", views.post_search, name="post_search"),
]

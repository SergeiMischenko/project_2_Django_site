from django.urls import path

from . import views

urlpatterns = [
    path("", views.CatsHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.contact, name="contact"),
    path("post/<slug:post_slug>/", views.PostView.as_view(), name="post"),
    path("posts/<slug:user_name>/", views.UserPosts.as_view(), name="user_posts"),
    path(
        "category/<slug:category_slug>/",
        views.CatsCategoryList.as_view(),
        name="category",
    ),
    path("tag/<slug:tag_slug>/", views.CatsTagList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
]

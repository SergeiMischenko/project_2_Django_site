from django.urls import path

from . import views

urlpatterns = [
    path('', views.CatsHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.PostView.as_view(), name='post'),
    path('category/<slug:category_slug>/', views.CatsCategoryList.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.CatsTagList.as_view(), name='tag'),
]

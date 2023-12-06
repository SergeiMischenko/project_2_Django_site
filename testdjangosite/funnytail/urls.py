from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<int:category_id>/', views.categories, name='category_id'),
]

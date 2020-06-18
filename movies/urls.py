from django.urls import path

from .views import MoviesListView, CategoriesListView, MoviesDetailView

urlpatterns = [
    path('movies/', MoviesListView.as_view()),
    path('movies/<id>', MoviesDetailView.as_view()),
    path('categories/', CategoriesListView.as_view()),
]

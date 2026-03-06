from django.urls import path

from .views import SongCategoryListView, SongDetailView, SongListView

app_name = 'songs'

urlpatterns = [
    path('categories/', SongCategoryListView.as_view(), name='category-list'),
    path('', SongListView.as_view(), name='song-list'),
    path('<int:pk>/', SongDetailView.as_view(), name='song-detail'),
]

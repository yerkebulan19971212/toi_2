from rest_framework import generics

from .models import Song, SongCategory
from .serializers import SongCategorySerializer, SongSerializer


class SongCategoryListView(generics.ListAPIView):
    queryset = SongCategory.objects.all()
    serializer_class = SongCategorySerializer


class SongListView(generics.ListAPIView):
    queryset = Song.objects.filter(is_active=True).select_related('category')
    serializer_class = SongSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.filter(is_active=True)
    serializer_class = SongSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Song.objects.filter(pk=instance.pk).update(play_count=instance.play_count + 1)
        serializer = self.get_serializer(instance)
        return generics.Response(serializer.data)

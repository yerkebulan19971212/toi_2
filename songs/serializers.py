from rest_framework import serializers

from .models import Song, SongCategory


class SongCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SongCategory
        fields = ['id', 'name', 'slug']


class SongSerializer(serializers.ModelSerializer):
    category_detail = SongCategorySerializer(source='category', read_only=True)
    duration_display = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = [
            'id', 'title', 'artist', 'audio', 'duration',
            'duration_display', 'category', 'category_detail',
            'cover_image', 'play_count',
        ]

    def get_duration_display(self, obj):
        return obj.duration_display()

    def get_audio(self, obj):
        if obj.audio_url:
            return obj.audio_url
        if obj.audio_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.audio_file.url)
        return None

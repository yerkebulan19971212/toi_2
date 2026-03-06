from django.contrib import admin

from .models import Song, SongCategory


@admin.register(SongCategory)
class SongCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'duration_display', 'play_count', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'artist')
    list_editable = ('is_active', 'order')
    readonly_fields = ('play_count', 'created_at')

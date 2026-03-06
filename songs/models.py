from django.db import models


class SongCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категориялар'

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=255, verbose_name='Ән атауы')
    artist = models.CharField(max_length=255, blank=True, verbose_name='Орындаушы')
    audio_file = models.FileField(
        upload_to='songs/', blank=True,
        verbose_name='Аудио файл'
    )
    audio_url = models.URLField(
        blank=True,
        help_text='Сыртқы аудио URL (файл жүктеудің орнына)',
        verbose_name='Аудио URL'
    )
    duration = models.PositiveIntegerField(
        default=0,
        help_text='Ұзақтығы секундпен',
        verbose_name='Ұзақтығы (сек)'
    )
    category = models.ForeignKey(
        SongCategory, related_name='songs',
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Категория'
    )
    cover_image = models.ImageField(
        upload_to='song_covers/', blank=True, null=True,
        verbose_name='Мұқаба суреті'
    )
    is_active = models.BooleanField(default=True, verbose_name='Белсенді')
    play_count = models.PositiveIntegerField(default=0, verbose_name='Ойнату саны')
    order = models.PositiveIntegerField(default=0, verbose_name='Реті')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Ән'
        verbose_name_plural = 'Әндер'

    def __str__(self):
        return f'{self.title} — {self.artist}' if self.artist else self.title

    def duration_display(self):
        mins = self.duration // 60
        secs = self.duration % 60
        return f'{mins}:{secs:02d}'

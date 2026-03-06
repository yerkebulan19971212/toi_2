from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тақырып')
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    excerpt = models.TextField(blank=True, verbose_name='Қысқаша мазмұн')
    content = models.TextField(verbose_name='Мазмұн')
    cover_image = models.ImageField(
        upload_to='blog/', blank=True, null=True,
        verbose_name='Мұқаба суреті'
    )
    is_published = models.BooleanField(default=False, verbose_name='Жарияланған')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Жарияланған күні')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Блог жазбасы'
        verbose_name_plural = 'Блог жазбалары'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            self.slug = base or f'post-{self.pk}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

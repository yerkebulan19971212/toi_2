import uuid

from django.db import models
from django.utils.text import slugify


class InvitationTemplate(models.Model):
    CATEGORY_CHOICES = [
        ('uzatu', 'Ұзату той'),
        ('qyz_uzatu', 'Қыз ұзату'),
        ('sunnet', 'Сүндет той'),
        ('tusaukesar', 'Тұсаукесер'),
        ('merey', 'Мерей той'),
        ('besik', 'Бесік той'),
        ('betashar', 'Беташар'),
        ('other', 'Асау тойлар'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='uzatu')
    preview_image = models.ImageField(upload_to='templates/', blank=True, null=True)
    gradient_from = models.CharField(max_length=20, default='#667eea')
    gradient_to = models.CharField(max_length=20, default='#764ba2')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name


class Invitation(models.Model):
    template = models.ForeignKey(
        InvitationTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField(unique=True, blank=True, max_length=120)
    bride_name = models.CharField(max_length=255)
    groom_name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    photo = models.ImageField(upload_to='invitations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f'{self.bride_name}-{self.groom_name}')
            self.slug = f'{base}-{uuid.uuid4().hex[:6]}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.bride_name} & {self.groom_name}'


class Guest(models.Model):
    STATUS_CHOICES = [
        ('yes', 'Қатысады'),
        ('no', 'Қатыса алмайды'),
        ('maybe', 'Әлі ойлануда'),
    ]

    invitation = models.ForeignKey(
        Invitation, related_name='guests', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='maybe')
    table_number = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.invitation.slug})'

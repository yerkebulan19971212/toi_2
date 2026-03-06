import uuid

from django.db import models
from django.utils.text import slugify

from base.abstract_models import NameModel


class InvitationCategory(NameModel):
    """Category for invitation templates (ұзату той, қыз ұзату, etc.)."""
    code = models.SlugField(max_length=32, unique=True)
    icon = models.CharField(max_length=128, blank=True, help_text='Icon class or emoji')
    subtitle = models.CharField(
        max_length=128, blank=True,
        help_text='Short subtitle shown under the category name (e.g. Үйлену)'
    )
    bg_class = models.CharField(
        max_length=128, blank=True, default='bg-emerald-50 group-hover:bg-emerald-100',
        help_text='Tailwind classes for the icon box, e.g. bg-amber-50 group-hover:bg-amber-100'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name_kz']
        verbose_name = 'Invitation category'
        verbose_name_plural = 'Invitation categories'

    def __str__(self):
        return self.name_kz or self.code


class InvitationTemplate(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'invitations.InvitationCategory',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='templates',
    )
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

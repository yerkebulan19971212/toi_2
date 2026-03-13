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
    """
    HTML template with Jinja2 variables.
    Only staff can create/edit templates.
    """
    IMAGE_LAYOUTS = [
        ('gallery_top', 'Gallery — Top'),
        ('gallery_bottom', 'Gallery — Bottom'),
        ('gallery_grid', '2×N Grid'),
        ('single_hero', 'Single Hero Image'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    category = models.ForeignKey(
        'invitations.InvitationCategory',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='templates',
    )
    description = models.TextField(blank=True)
    # Name of the Jinja2 HTML file in invitations/templates_html/ (without .html extension)
    template_file = models.CharField(
        max_length=100, blank=True,
        help_text='Filename (without .html) in invitations/templates_html/',
    )
    css_styles = models.TextField(blank=True, help_text='Scoped CSS injected into the template')
    # ["event_title","event_date","images","description", ...]
    supported_vars = models.JSONField(default=list, blank=True)
    # ["gallery_top","gallery_grid", ...]
    supported_image_layouts = models.JSONField(default=list, blank=True)
    form_schema = models.JSONField(default=dict, blank=True, help_text='Dynamic form field definitions')
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or f'template-{uuid.uuid4().hex[:6]}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    IMAGE_LAYOUTS = InvitationTemplate.IMAGE_LAYOUTS

    template = models.ForeignKey(
        InvitationTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=120)

    # --- Wedding-specific legacy fields (kept for backward compat) ---
    bride_name = models.CharField(max_length=255, blank=True)
    groom_name = models.CharField(max_length=255, blank=True)

    # --- Generic event fields ---
    event_title = models.CharField(max_length=300, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    # Extra template variables that don't have a dedicated column
    extra_data = models.JSONField(default=dict, blank=True)

    # Which image layout to use when rendering
    image_layout = models.CharField(
        max_length=50, choices=IMAGE_LAYOUTS, default='gallery_top'
    )

    # Cached rendered HTML — regenerated on save
    rendered_html = models.TextField(blank=True)

    photo = models.ImageField(upload_to='invitations/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.get_display_title())
            self.slug = f'{base}-{uuid.uuid4().hex[:6]}'
        super().save(*args, **kwargs)

    def get_display_title(self):
        if self.event_title:
            return self.event_title
        if self.bride_name and self.groom_name:
            return f'{self.bride_name}-{self.groom_name}'
        return self.bride_name or self.groom_name or 'invitation'

    def get_render_context(self):
        """Build the Jinja2 variable dict for this invitation."""
        images = list(
            self.images.values('url', 'placement', 'caption', 'sort_order')
        )
        return {
            'event_title': self.event_title or self.get_display_title(),
            'event_date': self.date.strftime('%d %B %Y') if self.date else '',
            'event_time': self.time.strftime('%H:%M') if self.time else '',
            'event_location': self.location,
            'map_link': self.map_url,
            'description': self.description,
            'images': images,
            'image_layout': self.image_layout,
            'bride_name': self.bride_name,
            'groom_name': self.groom_name,
            **self.extra_data,
        }

    def __str__(self):
        return self.get_display_title()


class InvitationImage(models.Model):
    PLACEMENTS = [
        ('gallery_top', 'Gallery Top'),
        ('gallery_bottom', 'Gallery Bottom'),
        ('gallery_grid', 'Gallery Grid'),
        ('single_hero', 'Single Hero'),
    ]

    invitation = models.ForeignKey(
        Invitation, on_delete=models.CASCADE, related_name='images'
    )
    url = models.URLField(max_length=1000)
    placement = models.CharField(
        max_length=50, choices=PLACEMENTS, default='gallery_top'
    )
    caption = models.CharField(max_length=300, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.placement} — {self.invitation}'


class GuestComment(models.Model):
    invitation = models.ForeignKey(
        Invitation, on_delete=models.CASCADE, related_name='comments'
    )
    guest_name = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.guest_name} → {self.invitation}'


class RSVPResponse(models.Model):
    CHOICES = [
        ('solo', 'Иә, жалғыз өзім барамын!'),
        ('with_partner', 'Жұбайыммен бірге барамын'),
        ('declined', 'Өкінішке орай, келе алмаймын'),
    ]

    invitation = models.ForeignKey(
        Invitation, on_delete=models.CASCADE, related_name='rsvp_responses'
    )
    guest_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, blank=True)
    response = models.CharField(max_length=20, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One RSVP per phone number per invitation
        unique_together = [('invitation', 'phone')]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.guest_name} ({self.get_response_display()})'


# Keep Guest model for the existing guest-list management feature
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

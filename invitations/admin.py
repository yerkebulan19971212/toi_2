from django.contrib import admin

from .models import (
    Guest,
    GuestComment,
    Invitation,
    InvitationCategory,
    InvitationImage,
    InvitationTemplate,
    RSVPResponse,
)


@admin.register(InvitationCategory)
class InvitationCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_kz', 'name_ru', 'subtitle', 'icon', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name_kz', 'name_ru', 'name_en', 'subtitle')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(InvitationTemplate)
class InvitationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'is_free', 'is_featured', 'is_active')
    list_filter = ('category', 'is_free', 'is_featured', 'is_active')
    search_fields = ('name', 'slug')
    list_editable = ('is_featured', 'is_active', 'is_free')
    readonly_fields = ('slug', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'preview_image', 'form_schema'),
        }),
        ('Template', {
            'fields': ('template_file', 'css_styles', 'supported_vars', 'supported_image_layouts'),
            'classes': ('wide',),
        }),
        ('Design', {
            'fields': ('gradient_from', 'gradient_to'),
        }),
        ('Pricing & Status', {
            'fields': ('price', 'is_free', 'is_featured', 'is_active', 'created_at'),
        }),

    )


class InvitationImageInline(admin.TabularInline):
    model = InvitationImage
    extra = 1
    fields = ('url', 'placement', 'caption', 'sort_order')


class GuestCommentInline(admin.TabularInline):
    model = GuestComment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('guest_name', 'comment', 'is_approved', 'created_at')


class RSVPResponseInline(admin.TabularInline):
    model = RSVPResponse
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('guest_name', 'phone', 'response', 'created_at')


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        'slug', 'get_display_title', 'date', 'location', 'is_published', 'created_at'
    )
    list_filter = ('date', 'is_published', 'image_layout')
    search_fields = ('bride_name', 'groom_name', 'event_title', 'slug')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    inlines = [InvitationImageInline, GuestCommentInline, RSVPResponseInline]
    fieldsets = (
        (None, {
            'fields': (
                'template', 'slug', 'is_published',
                'bride_name', 'groom_name', 'event_title',
            ),
        }),
        ('Event Details', {
            'fields': ('date', 'time', 'location', 'address', 'map_url', 'description'),
        }),
        ('Media', {
            'fields': ('photo', 'image_layout'),
        }),
        ('Extra Data', {
            'fields': ('extra_data',),
            'classes': ('collapse',),
        }),
        ('Rendered Output', {
            'fields': ('rendered_html',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Title')
    def get_display_title(self, obj):
        return obj.get_display_title()


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'invitation', 'status', 'table_number')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(GuestComment)
class GuestCommentAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'invitation', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    list_editable = ('is_approved',)
    search_fields = ('guest_name', 'comment')
    readonly_fields = ('created_at',)


@admin.register(RSVPResponse)
class RSVPResponseAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'phone', 'response', 'invitation', 'created_at')
    list_filter = ('response',)
    search_fields = ('guest_name', 'phone')
    readonly_fields = ('created_at',)

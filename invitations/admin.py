from django.contrib import admin

from .models import Guest, Invitation, InvitationCategory, InvitationTemplate


@admin.register(InvitationCategory)
class InvitationCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_kz', 'name_ru', 'icon', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name_kz', 'name_ru', 'name_en')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(InvitationTemplate)
class InvitationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_free', 'is_featured', 'is_active')
    list_filter = ('category', 'is_free', 'is_featured', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_featured', 'is_active', 'is_free')


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('slug', 'bride_name', 'groom_name', 'date', 'location', 'created_at')
    list_filter = ('date',)
    search_fields = ('bride_name', 'groom_name', 'slug')
    readonly_fields = ('slug', 'created_at', 'updated_at')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'invitation', 'status', 'table_number')
    list_filter = ('status',)
    search_fields = ('name',)

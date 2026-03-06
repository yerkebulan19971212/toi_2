from django.contrib import admin
from .models import Guest, Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("slug", "couple_names", "date", "location")


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("name", "invitation", "status", "table_number")
    list_filter = ("invitation", "status")

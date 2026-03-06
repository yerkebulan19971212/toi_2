from django.urls import path

from .views import GuestCreateView, InvitationDetailView

app_name = "invitations"

urlpatterns = [
    path("<slug:slug>/", InvitationDetailView.as_view(), name="detail"),
    path("<slug:slug>/guests/", GuestCreateView.as_view(), name="guest-create"),
]


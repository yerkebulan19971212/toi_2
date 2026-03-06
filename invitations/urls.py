from django.urls import path

from .views import (
    GuestCreateView,
    InvitationCreateView,
    InvitationDetailView,
    TemplateDetailView,
    TemplateListView,
)

app_name = 'invitations'

urlpatterns = [
    path('templates/', TemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),
    path('', InvitationCreateView.as_view(), name='invitation-create'),
    path('<slug:slug>/', InvitationDetailView.as_view(), name='invitation-detail'),
    path('<slug:slug>/guests/', GuestCreateView.as_view(), name='guest-create'),
]

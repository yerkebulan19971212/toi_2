from django.urls import path

from .views import (
    CategoryListView,
    GuestCommentListCreateView,
    GuestCreateView,
    InvitationCreateView,
    InvitationDetailView,
    InvitationHTMLView,
    InvitationQRView,
    MyInvitationsView,
    RSVPCreateView,
    RSVPResultsView,
    TemplateDetailView,
    TemplateListView,
)

app_name = 'invitations'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Templates
    path('templates/', TemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),

    # Invitations
    path('', InvitationCreateView.as_view(), name='invitation-create'),
    path('my/', MyInvitationsView.as_view(), name='my-invitations'),
    path('<slug:slug>/', InvitationDetailView.as_view(), name='invitation-detail'),

    # Legacy: guest-list management
    path('<slug:slug>/guests/', GuestCreateView.as_view(), name='guest-create'),

    # Public: comments
    path('<slug:slug>/comments/', GuestCommentListCreateView.as_view(), name='comment-list-create'),

    # Public: RSVP
    path('<slug:slug>/rsvp/', RSVPCreateView.as_view(), name='rsvp-create'),
    path('<slug:slug>/rsvp-results/', RSVPResultsView.as_view(), name='rsvp-results'),

    # QR code
    path('<slug:slug>/qr/', InvitationQRView.as_view(), name='invitation-qr'),
]

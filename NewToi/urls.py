from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from invitations.views import InvitationHTMLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls', namespace='accounts')),
    path('api/invitations/', include('invitations.urls', namespace='invitations')),
    path('api/songs/', include('songs.urls', namespace='songs')),
    path('api/blog/', include('blog.urls', namespace='blog')),
    # Direct HTML render for invitation (before SPA catchall)
    path('i/<slug:slug>/', InvitationHTMLView.as_view(), name='invitation-html'),
    path('', TemplateView.as_view(template_name='index.html'), name='spa'),
    path('<path:slug>/', TemplateView.as_view(template_name='index.html'), name='spa-catchall'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

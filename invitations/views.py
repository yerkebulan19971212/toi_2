import io

import qrcode
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import notify_comment, notify_rsvp
from .models import (
    Guest,
    GuestComment,
    Invitation,
    InvitationCategory,
    InvitationImage,
    InvitationTemplate,
    RSVPResponse,
)
from .renderer import render_invitation
from .serializers import (
    GuestCommentSerializer,
    GuestSerializer,
    InvitationCategorySerializer,
    InvitationReadSerializer,
    InvitationTemplateSerializer,
    InvitationWriteSerializer,
    RSVPResponseSerializer,
    RSVPResultsSerializer,
)


# ---------------------------------------------------------------------------
# Categories & Templates
# ---------------------------------------------------------------------------

class CategoryListView(generics.ListAPIView):
    queryset = InvitationCategory.objects.filter(is_active=True)
    serializer_class = InvitationCategorySerializer


class TemplateListView(generics.ListAPIView):
    queryset = InvitationTemplate.objects.filter(is_active=True)
    serializer_class = InvitationTemplateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            if category.isdigit():
                qs = qs.filter(category_id=int(category))
            else:
                qs = qs.filter(category__code=category)
        print(qs.query)
        print('----')
        return qs


class TemplateDetailView(generics.RetrieveAPIView):
    queryset = InvitationTemplate.objects.filter(is_active=True)
    serializer_class = InvitationTemplateSerializer


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------

class InvitationCreateView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = request.user if request.user.is_authenticated else None
        invitation = serializer.save(owner=owner)

        photos = request.FILES.getlist('photos')
        for i, photo in enumerate(photos):
            path = default_storage.save(f'invitations/photos/{photo.name}', photo)
            url = default_storage.url(path)
            InvitationImage.objects.create(
                invitation=invitation,
                url=url,
                placement=invitation.image_layout or 'gallery_top',
                sort_order=i,
            )

        if photos and invitation.template and invitation.template.template_file:
            ctx = invitation.get_render_context()
            invitation.rendered_html = render_invitation(invitation.template.template_file, ctx)
            invitation.save(update_fields=['rendered_html'])

        read_serializer = InvitationReadSerializer(
            invitation, context={'request': request}
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class MyInvitationsView(generics.ListAPIView):
    serializer_class = InvitationReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.prefetch_related('images').filter(owner=self.request.user)


class InvitationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Invitation.objects.prefetch_related('images', 'guests').all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return InvitationWriteSerializer
        return InvitationReadSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # always allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        read_serializer = InvitationReadSerializer(
            invitation, context={'request': request}
        )
        return Response(read_serializer.data)


# ---------------------------------------------------------------------------
# Guest list management (existing feature)
# ---------------------------------------------------------------------------

class GuestCreateView(generics.CreateAPIView):
    serializer_class = GuestSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)


# ---------------------------------------------------------------------------
# Guest Comments
# ---------------------------------------------------------------------------

class GuestCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = GuestCommentSerializer

    def get_queryset(self):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        return GuestComment.objects.filter(
            invitation=invitation, is_approved=True
        )

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        comment = serializer.save(invitation=invitation)
        notify_comment(invitation, comment)


# ---------------------------------------------------------------------------
# RSVP
# ---------------------------------------------------------------------------

class RSVPCreateView(generics.CreateAPIView):
    serializer_class = RSVPResponseSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        rsvp = serializer.save(invitation=invitation)
        notify_rsvp(invitation, rsvp)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception:
            # unique_together violation — phone already responded
            return Response(
                {'detail': 'Сіз бұрын жауап бергенсіз.'},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RSVPResultsView(APIView):
    """Aggregated RSVP counts for an invitation."""

    def get(self, request, slug):
        invitation = get_object_or_404(Invitation, slug=slug)
        counts = (
            invitation.rsvp_responses
            .values('response')
            .annotate(count=Count('id'))
        )
        result = {row['response']: row['count'] for row in counts}
        data = {
            'solo':         result.get('solo', 0),
            'with_partner': result.get('with_partner', 0),
            'declined':     result.get('declined', 0),
            'total_guests': result.get('solo', 0) + result.get('with_partner', 0) * 2,
        }
        return Response(RSVPResultsSerializer(data).data)


# ---------------------------------------------------------------------------
# Public invitation HTML page
# ---------------------------------------------------------------------------


class InvitationQRView(APIView):
    """Return a QR code PNG for the public invitation URL."""
    permission_classes = []

    def get(self, request, slug):
        get_object_or_404(Invitation, slug=slug)
        url = request.build_absolute_uri(f'/i/{slug}/')
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return HttpResponse(buf.getvalue(), content_type='image/png')


class InvitationAnalyticsView(APIView):
    """View + RSVP stats for an invitation. Owner-only."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        invitation = get_object_or_404(Invitation, slug=slug, owner=request.user)
        rsvp_counts = (
            invitation.rsvp_responses
            .values('response')
            .annotate(count=Count('id'))
        )
        rsvp = {row['response']: row['count'] for row in rsvp_counts}
        return Response({
            'view_count': invitation.view_count,
            'rsvp': {
                'solo':         rsvp.get('solo', 0),
                'with_partner': rsvp.get('with_partner', 0),
                'declined':     rsvp.get('declined', 0),
                'total_guests': rsvp.get('solo', 0) + rsvp.get('with_partner', 0) * 2,
            },
            'comments_count': invitation.comments.filter(is_approved=True).count(),
        })


def _build_og_tags(request, invitation):
    title = invitation.get_display_title()
    parts = []
    if invitation.date:
        parts.append(invitation.date.strftime('%d.%m.%Y'))
    if invitation.location:
        parts.append(invitation.location)
    description = ' · '.join(parts) if parts else 'Той шақыруы'

    page_url = request.build_absolute_uri(f'/i/{invitation.slug}/')

    # Image: invitation photo → template preview → fallback empty
    image_url = ''
    if invitation.photo:
        image_url = request.build_absolute_uri(invitation.photo.url)
    elif invitation.template and invitation.template.preview_image:
        image_url = request.build_absolute_uri(invitation.template.preview_image.url)

    def e(s):
        return str(s).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

    tags = f'''<meta property="og:type" content="website" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(description)}" />
<meta property="og:url" content="{e(page_url)}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{e(title)}" />
<meta name="twitter:description" content="{e(description)}" />'''

    if image_url:
        tags += f'\n<meta property="og:image" content="{e(image_url)}" />'
        tags += f'\n<meta name="twitter:image" content="{e(image_url)}" />'

    return tags


class InvitationHTMLView(APIView):
    """Render invitation HTML page with RSVP form."""
    permission_classes = []

    def get(self, request, slug):
        from .renderer import render_invitation
        invitation = get_object_or_404(Invitation, slug=slug)

        if invitation.template and invitation.template.template_file:
            ctx = invitation.get_render_context()
            try:
                html = render_invitation(invitation.template.template_file, ctx)
            except Exception:
                html = invitation.rendered_html or ''
        else:
            html = invitation.rendered_html or ''

        if not html:
            html = '<html><body style="font-family:sans-serif;text-align:center;padding:3rem"><p>Шаблон жоқ</p></body></html>'

        # Track view (atomic to avoid race conditions)
        Invitation.objects.filter(pk=invitation.pk).update(
            view_count=models.F('view_count') + 1
        )

        # Inject OG meta tags into <head>
        og_tags = _build_og_tags(request, invitation)
        if '<head>' in html:
            html = html.replace('<head>', f'<head>\n{og_tags}', 1)
        elif '</head>' in html:
            html = html.replace('</head>', f'{og_tags}\n</head>', 1)
        else:
            html = f'<head>{og_tags}</head>' + html

        return HttpResponse(html, content_type='text/html; charset=utf-8')

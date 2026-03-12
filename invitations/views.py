from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Guest,
    GuestComment,
    Invitation,
    InvitationCategory,
    InvitationTemplate,
    RSVPResponse,
)
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
        invitation = serializer.save()
        # Return full read representation after creation
        read_serializer = InvitationReadSerializer(
            invitation, context={'request': request}
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


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
        serializer.save(invitation=invitation)


# ---------------------------------------------------------------------------
# RSVP
# ---------------------------------------------------------------------------

class RSVPCreateView(generics.CreateAPIView):
    serializer_class = RSVPResponseSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)

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

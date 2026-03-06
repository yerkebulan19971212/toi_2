from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Guest, Invitation, InvitationCategory, InvitationTemplate
from .serializers import (
    GuestSerializer,
    InvitationCategorySerializer,
    InvitationSerializer,
    InvitationTemplateSerializer,
)


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


class InvitationCreateView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer


class InvitationDetailView(generics.RetrieveAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    lookup_field = 'slug'


class GuestCreateView(generics.CreateAPIView):
    serializer_class = GuestSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)

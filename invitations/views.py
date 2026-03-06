from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Guest, Invitation
from .serializers import GuestSerializer, InvitationSerializer


class InvitationDetailView(generics.RetrieveAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    lookup_field = "slug"


class GuestCreateView(generics.CreateAPIView):
    serializer_class = GuestSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs["slug"])
        serializer.save(invitation=invitation)


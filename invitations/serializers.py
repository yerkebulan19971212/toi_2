from rest_framework import serializers

from .models import Guest, Invitation


class GuestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Guest
    fields = [
        "id",
        "name",
        "phone",
        "status",
        "table_number",
        "notes",
        "created_at",
    ]


class InvitationSerializer(serializers.ModelSerializer):
  guests = GuestSerializer(many=True, read_only=True)

  class Meta:
    model = Invitation
    fields = [
        "id",
        "slug",
        "title",
        "couple_names",
        "date",
        "time",
        "location",
        "description",
        "guests",
    ]


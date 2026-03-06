from rest_framework import serializers

from .models import Guest, Invitation, InvitationTemplate


class InvitationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationTemplate
        fields = [
            'id', 'name', 'category', 'preview_image',
            'gradient_from', 'gradient_to', 'price', 'is_free',
            'is_featured', 'is_active', 'created_at',
        ]


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name', 'phone', 'status', 'table_number', 'notes', 'created_at']


class InvitationSerializer(serializers.ModelSerializer):
    guests = GuestSerializer(many=True, read_only=True)
    template_detail = InvitationTemplateSerializer(source='template', read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'id', 'slug', 'bride_name', 'groom_name',
            'date', 'time', 'location', 'address', 'map_url',
            'photo', 'template', 'template_detail',
            'guests', 'created_at',
        ]
        read_only_fields = ['slug', 'created_at']

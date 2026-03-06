from rest_framework import serializers

from .models import Guest, Invitation, InvitationCategory, InvitationTemplate


class InvitationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCategory
        fields = [
            'id', 'code', 'name_kz', 'name_ru', 'name_en',
            'icon', 'subtitle', 'bg_class', 'order', 'is_active',
        ]


class InvitationTemplateSerializer(serializers.ModelSerializer):
    category_detail = InvitationCategorySerializer(source='category', read_only=True)

    class Meta:
        model = InvitationTemplate
        fields = [
            'id', 'name', 'category', 'category_detail', 'preview_image',
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

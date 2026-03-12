from rest_framework import serializers

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
            'id', 'name', 'slug', 'description', 'category', 'category_detail',
            'supported_vars', 'supported_image_layouts',
            'preview_image', 'gradient_from', 'gradient_to',
            'price', 'is_free', 'is_featured', 'is_active', 'created_at',
        ]


class InvitationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationImage
        fields = ['id', 'url', 'placement', 'caption', 'sort_order']


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name', 'phone', 'status', 'table_number', 'notes', 'created_at']


# ---------------------------------------------------------------------------
# Invitation — read
# ---------------------------------------------------------------------------

class InvitationReadSerializer(serializers.ModelSerializer):
    guests = GuestSerializer(many=True, read_only=True)
    images = InvitationImageSerializer(many=True, read_only=True)
    template_detail = InvitationTemplateSerializer(source='template', read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'id', 'slug',
            'template', 'template_detail',
            'bride_name', 'groom_name',
            'event_title', 'date', 'time',
            'location', 'address', 'map_url',
            'description', 'extra_data',
            'image_layout', 'images',
            'rendered_html', 'is_published',
            'photo', 'guests', 'created_at', 'updated_at',
        ]


# ---------------------------------------------------------------------------
# Invitation — create / update
# ---------------------------------------------------------------------------

class InvitationWriteSerializer(serializers.ModelSerializer):
    images = InvitationImageSerializer(many=True, required=False)

    class Meta:
        model = Invitation
        fields = [
            'template',
            'bride_name', 'groom_name',
            'event_title', 'date', 'time',
            'location', 'address', 'map_url',
            'description', 'extra_data',
            'image_layout', 'images',
            'photo', 'is_published',
        ]

    def _save_images(self, invitation, images_data):
        invitation.images.all().delete()
        for img in images_data:
            InvitationImage.objects.create(invitation=invitation, **img)

    def _render_and_cache(self, invitation):
        if invitation.template and invitation.template.html_template:
            ctx = invitation.get_render_context()
            invitation.rendered_html = render_invitation(
                invitation.template.html_template, ctx
            )
            invitation.save(update_fields=['rendered_html'])

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        invitation = Invitation.objects.create(**validated_data)
        self._save_images(invitation, images_data)
        self._render_and_cache(invitation)
        return invitation

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            self._save_images(instance, images_data)
        self._render_and_cache(instance)
        return instance


# ---------------------------------------------------------------------------
# GuestComment
# ---------------------------------------------------------------------------

class GuestCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestComment
        fields = ['id', 'guest_name', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


# ---------------------------------------------------------------------------
# RSVP
# ---------------------------------------------------------------------------

class RSVPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVPResponse
        fields = ['id', 'guest_name', 'phone', 'response', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_phone(self, value):
        # If phone provided, check uniqueness per invitation (handled by unique_together,
        # but give a friendlier error here)
        return value


class RSVPResultsSerializer(serializers.Serializer):
    solo = serializers.IntegerField()
    with_partner = serializers.IntegerField()
    declined = serializers.IntegerField()
    total_guests = serializers.IntegerField()

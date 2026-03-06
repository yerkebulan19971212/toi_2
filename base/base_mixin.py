from typing import Any, Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class MethodMatchingViewSetMixin:
    action_serializers = None

    def get_serializer_class(self):
        base_serializer = super(MethodMatchingViewSetMixin,
                                self).get_serializer_class()
        return self.get_action_serializer_class().get(self.action,
                                                      base_serializer)

    def get_action_serializer_class(self) -> Dict[str, Any]:
        return self.action_serializers or {}


class BaseListModelMixin:
    """
    List a queryset.
    """

    def list_response(self, request, page_length=0, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if page_length > 0:
            queryset = queryset[:page_length]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create_new_obj(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

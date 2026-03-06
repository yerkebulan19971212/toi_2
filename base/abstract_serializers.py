from rest_framework.serializers import ModelSerializer, SerializerMethodField


class GetNameSerializer(ModelSerializer):
    name = SerializerMethodField()

    def get_name(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('lang')
        if lang == 'ru':
            return obj.name_ru
        return obj.name_kz


class GetNameDictSerializer(ModelSerializer):
    name = SerializerMethodField()

    def get_name(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('lang')
        if lang == 'ru':
            return obj['name_ru']
        return obj['name_kz']

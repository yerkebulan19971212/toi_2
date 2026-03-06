import django_filters
from accounts.models import User
from django.db.models import Q
from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters
from news.models import CommentNews
from quizzes.models import (Answer, Lesson, Question, Topic,
                            UserQuestionAnswer, VideoUrl)
from universities.models import University


class LessonFilter(django_filters.FilterSet):
    q = CharFilter(method='search_filter')

    class Meta:
        model = Lesson
        fields = ('test_type', 'video', 'probnyi')

    @staticmethod
    def search_filter(queryset, name, value):
        queryset = queryset.filter(
            Q(name_kz__icontains=value.capitalize()) |
            Q(name_ru__icontains=value.capitalize()) |
            Q(name_en__icontains=value.capitalize()) |
            Q(name_kz__icontains=value) |
            Q(name_ru__icontains=value) |
            Q(name_en__icontains=value)
        )
        return queryset


class TopicFilter(filters.FilterSet):
    speciality = filters.NumberFilter(field_name="lesson_topics__lesson_id", required=True)
    q = CharFilter(method='search_filter')

    class Meta:
        model = Topic
        fields = [
            'speciality'
        ]

    @staticmethod
    def search_filter(queryset, name, value):
        queryset = queryset.filter(
            Q(name_kz__icontains=value.capitalize()) |
            Q(name_ru__icontains=value.capitalize()) |
            Q(name_en__icontains=value.capitalize()) |
            Q(name_kz__icontains=value) |
            Q(name_ru__icontains=value) |
            Q(name_en__icontains=value)
        )
        return queryset


class QuestionOnlyTopicFilter(filters.FilterSet):
    lesson = filters.NumberFilter(field_name="topic_id")
    q = CharFilter(method='search_filter')

    class Meta:
        model = Question
        fields = ['lesson']

    @staticmethod
    def search_filter(queryset, name, value):
        queryset = queryset.filter(
            Q(question__icontains=value.capitalize()) |
            Q(common_question__text__icontains=value.capitalize())
        )
        return queryset


class QuestionLessonFilter(filters.FilterSet):
    speciality = filters.NumberFilter(field_name="topic__lesson_topics__lesson_id", required=True)

    class Meta:
        model = Question
        fields = ['speciality']


class AnswerFilter(filters.FilterSet):
    class Meta:
        model = Answer
        fields = ['question']


class UserTestQuestionFilter(filters.FilterSet):
    class Meta:
        model = UserQuestionAnswer
        fields = ['test']


class UserRatingFilter(filters.FilterSet):
    lesson = NumberFilter(method='rating_filter')
    q = CharFilter(method='search_filter')

    @staticmethod
    def search_filter(queryset, name, value):
        queryset = queryset.filter(
            Q(phone__icontains=value.capitalize()) |
            Q(email__icontains=value.capitalize()) |
            Q(first_name__icontains=value.capitalize()) |
            Q(last_name__icontains=value.capitalize())
        )
        return queryset

    class Meta:
        model = User
        fields = []

    @staticmethod
    def rating_filter(queryset, name, value):
        return queryset


class GetALLCommentFilter(django_filters.FilterSet):
    class Meta:
        model = CommentNews
        fields = (
            'news',
        )


class VideoUrlFilter(filters.FilterSet):
    lang = CharFilter(method='search_filter')

    class Meta:
        model = VideoUrl
        fields = [
            'lesson',
            'lang'
        ]

    @staticmethod
    def search_filter(queryset, name, value):
        lang = value.upper()
        queryset = queryset.filter(lang=lang)
        return queryset


class UniversityFilter(filters.FilterSet):
    q = CharFilter(method='search_filter')

    class Meta:
        model = University
        fields = ['q']

    @staticmethod
    def search_filter(queryset, name, value):
        queryset = queryset.filter(
            Q(name_kz__icontains=value) |
            Q(name_ru__icontains=value) |
            Q(name_en__icontains=value)
        )
        print(queryset.query)
        print(".query")
        return queryset

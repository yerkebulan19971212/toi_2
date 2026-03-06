from enum import Enum

from django.utils.translation import gettext_lazy as _

ANSWER_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']


class Choice(Enum):
    @classmethod
    def choices(cls):
        return [(c.value, _(c.name)) for c in cls]

    @classmethod
    def repr(cls):
        return {c.name: {'id': c.value, 'name': _(c.name)} for c in cls}

    @classmethod
    def list(cls):
        return [c.value for c in cls]

    def __str__(self):
        return self.value


class AnswerChoiceType(str, Choice):
    CHOICE = 'CHOICE'
    MULTICHOICE = 'MULTICHOICE'


class Language(str, Choice):
    KZ = 'KZ'
    RU = 'RU'


class QuestionType(str, Choice):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'


class TopicQuestionType(str, Choice):
    READING = 'READING'
    GRAMMAR = 'GRAMMAR'
    LISTENING = 'LISTENING'


class TopicType(str, Choice):
    FIRST = 'FIRST'
    SECOND = 'SECOND'


class QuizzStatus(str, Choice):
    NOT_PASSED = 'NOT_PASSED'
    CONTINUE = 'CONTINUE'
    PASSED = 'PASSED'
    EXPIRED = 'EXPIRED'


class LessonStatus(str, Choice):
    INACTIVE = "INACTIVE"
    ACTIVE = 'ACTIVE'
    SOON = "SOON"


class QuestionShowType(str, Choice):
    RANDOM = "RANDOM"
    THEORY = 'THEORY'
    PRACTICE = "PRACTICE"
    MASTERED = "MASTERED"


class MasteredType(str, Choice):
    TEN = "TEN"
    TWO = 'TWO'
    FIVE = 'FIVE'
    TWENTY_FIVE = 'TWENTY_FIVE'
    THIRTY_TWO = 'THIRTY_TWO'


class VideoType(str, Choice):
    STREAM = "STREAM"
    VIDEO = 'VIDEO'

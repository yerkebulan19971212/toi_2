import openai
import random
import string
import time
from datetime import datetime

import pytz
import requests
from django.conf import settings
from openai import OpenAI
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from quizzes.models import Lesson, Topic

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_path_upload_avatar(instance, file):
    """Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg
    """
    return f'avatar/{instance.id}/{file}'


def validate_size_image(file_obj):
    """Проверка размера файла
    """
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {megabyte_limit}MB')


def get_now_datetime():
    tz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(tz=tz)
    return now


def get_datetime_now_today_yesterday(now_utc):
    almaty_tz = pytz.timezone("Asia/Almaty")
    now_almaty = now_utc.astimezone(almaty_tz)

    start_today_almaty = now_almaty.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today_almaty = now_almaty.replace(hour=23, minute=59, second=59, microsecond=999999)

    start_today = start_today_almaty.astimezone(pytz.utc)
    end_today = end_today_almaty.astimezone(pytz.utc)
    return now_almaty, start_today, end_today


def bad_request_response(message=""):
    return Response({
        "message": message
    }, status=status.HTTP_400_BAD_REQUEST)


def generate_promo_code():
    code_length = 6
    chars = string.ascii_letters + string.digits

    my_seed = random.randint(0, 99)
    random.seed(time.time() + my_seed)

    code = ''.join(random.choice(chars) for _ in range(code_length))
    return code


def get_correct_answer_count(a, b):
    result = list(filter(lambda x: x in a, b))
    return len(result)


def get_multi_score(correct_p, answer_p):
    correct_p = [ans.id for ans in correct_p]
    answer_p = [ans.id for ans in answer_p]
    correct_answer_count = get_correct_answer_count(correct_p, answer_p)
    if len(correct_p) == 1 and correct_answer_count == 1:
        if len(answer_p) == 1:
            return 2
        elif len(answer_p) == 2:
            return 1
    elif len(correct_p) != 1:
        if len(correct_p) == len(answer_p) == correct_answer_count:
            return 2
        elif (len(answer_p) == len(
                correct_p) - 1 and correct_answer_count == len(
            correct_p) - 1) or (
                len(answer_p) == len(
            correct_p) + 1 and correct_answer_count == len(correct_p)):
            return 1
        elif ((len(correct_p) == len(answer_p)) or len(correct_p) == (
                len(answer_p))) and (
                correct_answer_count == len(correct_p) - 1):
            return 1
    return 0


def get_by_pagination(page, per_size, all_items):
    start = (page - 1) * per_size
    end = start + per_size
    return all_items[start:end]


def get_question_text_answer(question, lang):
    topic = Topic.objects.filter(id=question.topic_id).first()
    common = question.common_question
    common_text = ""
    if common:
        common_text = common.text if common.text else ""
    if lang == "kz":
        prompt = topic.prompt_kz
    else:
        prompt = topic.prompt_ru
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": common_text + question.question}
        ]
    )
    return completion.choices[0].message.content


def send_push_token(title, text, to_tokens, user_pushs):
    from accounts.models import UserPushNotification

    url = "https://exp.host/--/api/v2/push/send"

    response = requests.post(
        url,
        json={
            "to": to_tokens,
            "title": title,
            "body": text
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code != 200:
        UserPushNotification.objects.bulk_create(user_pushs)

    print(response.status_code)
    print(response.json())
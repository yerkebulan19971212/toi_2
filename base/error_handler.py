from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.data.get('message'):
            response.data['message'] = response.data['message'][0]

    return response

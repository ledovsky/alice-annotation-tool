import os
import telebot

from rest_framework.views import exception_handler

print(os.environ)
bot_token = os.environ.get('DJANGO_TELEGRAM_TOKEN')
bot_group_id = None
if bot_token:
    bot_group_id = int(os.environ['DJANGO_TELEGRAM_GROUP_ID'])


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # send error message if bot token is provided
    if bot_token:
        bot = telebot.TeleBot(bot_token)
        detail = exc.args[0]
        if response:
            detail = response.data['detail']
        message = f'Status code : {response.status_code}\nError message:\n{detail}'
        bot.send_message(bot_group_id, message)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
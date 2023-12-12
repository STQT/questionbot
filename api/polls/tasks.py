import logging

import requests

from celery import shared_task
from django.conf import settings
from django.shortcuts import get_object_or_404

from api.polls.models import Poll

TOKEN = settings.TELEGRAM_BOT_TOKEN
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'

@shared_task
def update_vote_message(message_id, channel_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    inline_keyboard = []
    choices_dict = poll.get_choice_counts()
    url = 'https://t.me/' + settings.TELEGRAM_USERNAME + "?start=poll" + str(poll_id)
    for choice in choices_dict:
        inline_keyboard.append([{"text": choice['text'] + f" {choice['vote_count']}",
                                 "url": url}])
    message = {
        'chat_id': channel_id,
        'message_id': int(message_id),
        'reply_markup': {
            'inline_keyboard': inline_keyboard
        },
    }
    url = f'https://api.telegram.org/bot{TOKEN}/editMessageReplyMarkup'
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return True
    logging.error(
        f"Poll id: {poll_id}, Message id: {message_id}, Channel id: {channel_id}, \n"
        f"tg response: {response.json()}")
    return False

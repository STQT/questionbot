import json

from django.conf import settings
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import generics
from django.contrib import messages
from rest_framework.views import APIView, Response

from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer

import requests

from .tasks import update_vote_message
from ..channels.models import Channel
from ..channels.serializers import ChannelListSerializer


class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.prefetch_related("choices")
    serializer_class = PollSerializer


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        vote = serializer.save()
        update_vote_message.delay(vote.poll.message_id, vote.poll.channel.channel_id, vote.poll_id)


class PollOwnerChatsView(APIView):
    serializer_class = ChannelListSerializer

    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        channels = Channel.objects.filter(owner=poll.owner, is_active=True)
        serializer = self.serializer_class(channels, many=True)
        return Response(serializer.data)


api_token = settings.TELEGRAM_BOT_TOKEN
base_url = f'https://api.telegram.org/bot{api_token}'
SEND_MEDIA = f"https://api.telegram.org/bot{api_token}/sendMediaGroup"


def send_media_group(text, chat_id, media, reply_markup=None):
    api_url = f'{base_url}/sendPhoto'
    params = {
        'chat_id': chat_id,
        'caption': text,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps({'inline_keyboard': reply_markup})
    }
    with open(media, 'rb') as photo:
        files = {'photo': (photo.name, photo)}
        response = requests.post(api_url, params=params, files=files)
    return response


def send_notifications_text(text, chat_id, reply_markup=None):
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    data = {'chat_id': chat_id, 'reply_markup': {'inline_keyboard': reply_markup}, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(url, json=data)
    return response


def poll_send(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    poll = get_object_or_404(Poll, pk=pk)
    if poll.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this poll.")
    message_text = poll.text.replace("<br />", "\n")

    url = 'https://t.me/' + settings.TELEGRAM_USERNAME + "?start=poll" + str(pk)

    # Create the inline keyboard
    inline_keyboard = []
    for choice in poll.choices.all():
        inline_keyboard.append([{"text": choice.text, "url": url}])

    if not inline_keyboard:
        messages.error(request, "So'rovnomada bironta javob mavjud emas iltimos xatoni to'g'irlang")
        return redirect(reverse('admin:polls_poll_changelist'))

    channel = poll.channel
    if poll.photo:
        cache_path = settings.MEDIA_ROOT
        compressed_image = poll.photo_compress.url
        compressed_image_path = cache_path + compressed_image[len(settings.MEDIA_URL):]
        response = send_media_group(text=message_text,
                                    chat_id=channel.channel_id,
                                    media=compressed_image_path,
                                    reply_markup=inline_keyboard)
    else:
        response = send_notifications_text(text=message_text,
                                           chat_id=channel.channel_id,
                                           reply_markup=inline_keyboard)
    if response.status_code == 200:
        poll.message_id = str(response.json()['result']['message_id'])
        poll.is_sent = True
        poll.save()
        messages.success(request, "Xabar " + channel.name + " ga muvaffaqiyatli yuborildi")
    else:
        messages.error(request, "Telegram serverida xatolik bo'ldi. Kanal " + channel.name + "ga xabar bormadi")

    return redirect(reverse('admin:polls_poll_changelist'))

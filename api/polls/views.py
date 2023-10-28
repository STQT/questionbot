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

from ..channels.models import Channel
from ..channels.serializers import ChannelListSerializer


class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.prefetch_related("choices")
    serializer_class = PollSerializer


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class PollOwnerChatsView(APIView):
    serializer_class = ChannelListSerializer
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        channels = Channel.objects.filter(owner=poll.owner, is_active=True)
        serializer = self.serializer_class(channels, many=True)
        return Response(serializer.data)



def poll_send(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    poll = get_object_or_404(Poll, pk=pk)
    if poll.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this poll.")
    bot_token = settings.TELEGRAM_BOT_TOKEN
    message_text = poll.text

    # Replace 'YOUR_URL' with the URL you want to attach to the inline keyboard
    url = 'https://t.me/' + settings.TELEGRAM_USERNAME + "?start=poll" + str(pk)

    # Create the inline keyboard
    inline_keyboard = []
    for choice in poll.choices.all():
        inline_keyboard.append([{"text": choice.text, "url": url}])

    if not inline_keyboard:
        messages.error(request, "So'rovnomada bironta javob mavjud emas iltimos xatoni to'g'irlang")
        return redirect(reverse('admin:polls_poll_changelist'))

    channel = poll.channel
    message = {
        'chat_id': channel.channel_id,
        'text': message_text,
        'reply_markup': {
            'inline_keyboard': inline_keyboard
        },
        'parse_mode': 'HTML'
    }

    # Send the message using the Telegram Bot API
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    response = requests.post(url, json=message)

    # Check if the message was sent successfully
    if response.status_code == 200:
        poll.message_id = str(response.json()['result']['message_id'])
        poll.is_sent = True
        poll.save()
        messages.success(request, "Xabar " + channel.name + " ga muvaffaqiyatli yuborildi")
    else:
        messages.error(request, "Telegram serverida xatolik bo'ldi. Kanal " + channel.name + "ga xabar bormadi")

    return redirect(reverse('admin:polls_poll_changelist'))

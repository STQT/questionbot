import pytz
from django.conf import settings
from django.utils import timezone

from rest_framework import serializers
from .models import Poll, Choice, Vote
from ..channels.serializers import ChannelListSerializer
from ..users.models import Voter


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, data):
        poll = data['poll']
        user = data['user']
        _voter, _created = Voter.objects.get_or_create(id=user.id)
        if Vote.objects.filter(user=user, poll=poll).exists():
            raise serializers.ValidationError('You have already voted for this poll.')
        if poll.closed_at and timezone.localtime(timezone.now(), pytz.timezone(settings.TIME_ZONE)) > poll.closed_at:
            raise serializers.ValidationError('This poll has already ended.')
        return data

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
    user = serializers.PrimaryKeyRelatedField(queryset=Voter.objects.all()[:5], required=False)
    user_id = serializers.IntegerField(write_only=True)
    choice_text = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = '__all__'

    def get_choice_text(self, obj):
        return obj.choice.text

    def validate(self, data):
        poll = data['poll']
        user_id = data['user_id']

        voter, _created = Voter.objects.get_or_create(id=user_id)
        vote = Vote.objects.filter(user=voter, poll=poll).select_related("choice")
        if vote.exists():
            raise serializers.ValidationError(
                {"poll": f"Siz allaqachon ushbu <b>{vote.first().choice.text}</b> javobni tanlab bo'lgansiz"})
        if poll.closed_at and timezone.localtime(timezone.now(), pytz.timezone(settings.TIME_ZONE)) > poll.closed_at:
            raise serializers.ValidationError({"poll": "Ushbu so'rovnoma allaqachon tugagan"})
        data['user'] = voter
        return data

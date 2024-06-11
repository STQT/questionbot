from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User
from api.channels.models import Channel


class PollResource(resources.ModelResource):
    owner = fields.Field(
        column_name='owner',
        attribute='owner',
        widget=ForeignKeyWidget(User, 'username'))

    channel = fields.Field(
        column_name='channel',
        attribute='channel',
        widget=ForeignKeyWidget(Channel, 'name'))

    vote_count = fields.Field()

    class Meta:
        model = Poll
        fields = ('id', 'message_id', 'text', 'photo', 'created_at', 'closed_at', 'is_sent', 'owner', 'channel')

    def dehydrate_vote_count(self, poll):
        return poll.vote_set.count()


class ChoiceResource(resources.ModelResource):
    poll = fields.Field(
        column_name='poll',
        attribute='poll',
        widget=ForeignKeyWidget(Poll, 'text'))

    class Meta:
        model = Choice
        fields = ('id', 'poll', 'text')


class VoteResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username'))

    poll = fields.Field(
        column_name='poll',
        attribute='poll',
        widget=ForeignKeyWidget(Poll, 'text'))

    choice = fields.Field(
        column_name='choice',
        attribute='choice',
        widget=ForeignKeyWidget(Choice, 'text'))

    class Meta:
        model = Vote
        fields = ('id', 'user', 'poll', 'choice')

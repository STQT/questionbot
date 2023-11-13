from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.channels.models import Channel


User = get_user_model()

class OwnerField(serializers.CharField):
    def to_internal_value(self, data):
        try:
            user = User.objects.get(guid=data)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("CustomUser with this GUID does not exist.")

class ChannelSerializer(serializers.ModelSerializer):
    guid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Channel
        fields = '__all__'
        extra_kwargs = {
            "owner": {"read_only": True},
            "channel_id": {"required": True}
        }

    def create(self, validated_data):
        owner_guid = validated_data.pop('guid')
        try:
            owner = User.objects.get(guid=owner_guid)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesnt exists")
        if Channel.objects.filter(channel_id=validated_data['channel_id']).exists():
            raise serializers.ValidationError("Channel with this ID exists.")
        channel = Channel.objects.create(owner=owner, **validated_data)
        return channel
    # def validate(self, data):
    #     poll = data['poll']
    #     user = data['user']
    #     _voter, _created = Voter.objects.get_or_create(id=user.id)
    #     if Vote.objects.filter(user=user, poll=poll).exists():
    #         raise serializers.ValidationError('You have already voted for this poll.')
    #     if poll.closed_at and timezone.now() > poll.closed_at:
    #         raise serializers.ValidationError('This poll has already ended.')
    #     return data


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "channel_id", "name",
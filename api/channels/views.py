from rest_framework import generics

from api.channels.models import Channel
from api.channels.serializers import ChannelSerializer


class ChannelCreateView(generics.CreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

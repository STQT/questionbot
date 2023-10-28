from django import forms

from api.channels.models import Channel

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'owner', 'is_active', 'link']

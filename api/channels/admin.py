from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from api.channels.forms import ChannelForm
from api.channels.models import Channel
from api.contrib.admin import StaffAdmin


@admin.register(Channel)
class ChannelAdmin(StaffAdmin):
    app_model_string = "channels_channel"
    form = ChannelForm
    add_form_template = "channels/add_form.html"
    readonly_fields = ["channel_id"]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return "name", "channel_id", "owner", "is_active"
        return "name", "active_channel_column", "tools_column",

    def active_channel_column(self, obj):
        html_tag = 'Faol'
        if obj.is_active is False:
            html_tag = 'Nofaol'
        return html_tag

    active_channel_column.short_description = 'Faollik holati'
    active_channel_column.allow_tags = True

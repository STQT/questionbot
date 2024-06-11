import pytz

from django.conf import settings
from django.contrib import admin

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

from api.contrib.admin import StaffAdmin
from api.polls.forms import PollModelAdminForm
from api.polls.models import Poll, Choice, Vote
from import_export.admin import ImportExportModelAdmin
from api.polls.resources import ChoiceResource, PollResource, VoteResource

User = get_user_model()


class PollChoicesInline(admin.TabularInline):
    model = Choice
    extra = 2

    def has_change_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request, obj):
        if request.user.is_staff:
            return True
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return super().has_delete_permission(request, obj)


@admin.register(Poll)
class PollAdmin(ImportExportModelAdmin, StaffAdmin):
    inlines = [PollChoicesInline]
    app_model_string = "polls_poll"
    form = PollModelAdminForm
    resource_class = PollResource
    list_display = ('text', 'owner', 'channel', 'created_at', 'closed_at', 'is_sent')

    def save_model(self, request, obj, form, change):
        utc_time = obj.closed_at
        target_timezone = pytz.timezone(settings.TIME_ZONE)
        tashkent_time = utc_time.astimezone(target_timezone)
        obj.closed_at = tashkent_time
        obj.save()

    def truncated_text(self, obj):
        return obj.text[:50] if len(obj.text) > 50 else obj.text

    truncated_text.short_description = 'Savol matni'

    def get_list_display(self, request):
        if request.user.is_superuser:
            return "truncated_text", "owner", "closed_at", "send_column"
        return "truncated_text", "closed_at", "send_column", "tools_column",

    def send_column(self, obj):
        html_tag = "Yuborildi"
        if obj.is_sent is False:
            html_tag = '<a href="{0}" class="btn btn-success">Yuborish</a> '
        return mark_safe(
            html_tag.format(
                reverse('v1:polls:poll-send', args=[obj.pk]), )
        )

    send_column.short_description = 'Xabarni yuborish'
    send_column.allow_tags = True


@admin.register(Choice)
class ChoiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ChoiceResource
    list_display = ('text', 'poll', 'votes_count')
    list_filter = ('poll',)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def votes_count(self, obj):
        return obj.voting.all().count()

    votes_count.short_description = 'Ovoz soni'
    votes_count.allow_tags = True


@admin.register(Vote)
class VoteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VoteResource
    list_display = ('user', 'poll', 'choice')

    def has_module_permission(self, request):
        return request.user.is_superuser

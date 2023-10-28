from django.conf import settings
from django.contrib import admin
from django.forms import ModelChoiceField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth import get_user_model

from api.channels.models import Channel

User = get_user_model()


class StaffAdmin(admin.ModelAdmin):
    app_model_string = None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            if request.user.is_superuser:
                queryset = User.objects.all()
            else:
                queryset = User.objects.filter(pk=request.user.pk)
            return ModelChoiceField(queryset, initial=request.user)
        elif db_field.name == "channel":
            if request.user.is_superuser:
                queryset = Channel.objects.all()
            else:
                queryset = Channel.objects.filter(owner=request.user)
            return ModelChoiceField(queryset, initial=request.user)
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_staff:
            return True
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return super().has_delete_permission(request, obj)

    def tools_column(self, obj):
        assert self.app_model_string is not None, "The `app_model_string` attribute class StaffAdmin is not None"
        return mark_safe(
            '<a href="{0}" class="btn btn-primary">Tahrirlash</a> '
            '<a href="{1}" class="btn btn-danger">O\'chirish</a>'.format(
                reverse(f'admin:{self.app_model_string}_change', args=[obj.pk]),
                reverse(f'admin:{self.app_model_string}_delete', args=[obj.pk])
            ))

    tools_column.short_description = 'Boshqaruv'
    tools_column.allow_tags = True

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = dict(show_save_and_continue=False,
                             show_save_and_add_another=False,
                             telegram_username=settings.TELEGRAM_USERNAME,
                             owner_guid=request.user.guid
                             )
        template_response = super().add_view(request, form_url, extra_context)
        return template_response

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = dict(show_save_and_continue=False, show_save_and_add_another=False)
        template_response = super().change_view(request, object_id, form_url, extra_context)
        return template_response

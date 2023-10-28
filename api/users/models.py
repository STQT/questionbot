import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    guid = models.UUIDField(_("User UUID"), db_index=True, default=uuid.uuid4, editable=False)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})


class Voter(models.Model):
    id = models.IntegerField(_("Ovoz beruvchi ID"), primary_key=True, editable=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _("Ovoz beruvchi")
        verbose_name_plural = _("Ovoz beruvchilar")
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

from api.users.models import Voter

User = get_user_model()


class Poll(models.Model):
    message_id = models.CharField("Xabar ID", max_length=10, editable=False, db_index=True,
                                  null=True, blank=True)
    text = RichTextField(max_length=1023, verbose_name="Savol matni")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yaratuvchi")
    channel = models.ForeignKey("channels.Channel", verbose_name="Yuboriladigan kanal", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(verbose_name="Amal qilish muddati")
    is_sent = models.BooleanField(default=False, editable=False)

    class Meta:
        default_related_name = "polls"
        verbose_name = "Savol "
        verbose_name_plural = "Savollar "

    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name="Savol", on_delete=models.CASCADE)
    text = models.CharField(max_length=50, verbose_name="Javob")

    class Meta:
        default_related_name = "choices"
        verbose_name = "Javob "
        verbose_name_plural = "Javoblar "

    def __str__(self):
        return self.text


class Vote(models.Model):
    user = models.ForeignKey(Voter, verbose_name="Ovoz beruvchi", on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, verbose_name="Savol", on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, verbose_name="Javob", on_delete=models.CASCADE)

    class Meta:
        default_related_name = "voting"
        verbose_name = "Ovoz "
        verbose_name_plural = "Ovozlar "
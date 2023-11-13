from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Channel(models.Model):
    name = models.CharField(verbose_name="Kanal nomi", max_length=50)
    channel_id = models.CharField(verbose_name="Kanal ID", max_length=20, db_index=True)
    owner = models.ForeignKey(User, verbose_name="Egasi", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Faolmi?", default=False)
    link = models.CharField(
        verbose_name="Havola", max_length=100, help_text="Na'muna: @savolnoma yoki t.me/savolnoma")

    class Meta:
        default_related_name = "channels"
        verbose_name = "Kanal "
        verbose_name_plural = "Kanallar "

    def __str__(self):
        return self.name


# Generated by Django 4.1.9 on 2023-12-26 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0009_alter_channel_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Kanal nomi'),
        ),
    ]
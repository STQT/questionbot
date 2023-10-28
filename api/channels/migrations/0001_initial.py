# Generated by Django 4.1.9 on 2023-10-28 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Kanal nomi')),
                ('channel_id', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Kanal ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Kanal ',
                'verbose_name_plural': 'Kanallar ',
                'default_related_name': 'channels',
            },
        ),
    ]

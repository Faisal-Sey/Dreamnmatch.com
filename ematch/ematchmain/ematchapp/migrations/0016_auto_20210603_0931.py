# Generated by Django 2.2.17 on 2021-06-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ematchapp', '0015_remove_profile_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Ethnicity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 2.2.17 on 2021-05-29 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ematchapp', '0012_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Birthplace',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Interest_bands',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Interest_games',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Interest_movies',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Interest_shows',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_description',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_description1',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_end',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_end1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_started',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_started1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Jobs_title1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
# Generated by Django 2.2.17 on 2021-06-07 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ematchapp', '0025_status_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
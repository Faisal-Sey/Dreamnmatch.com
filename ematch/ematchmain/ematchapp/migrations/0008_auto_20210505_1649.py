# Generated by Django 2.2.17 on 2021-05-05 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ematchapp', '0007_auto_20210407_1138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qualities',
            old_name='eight',
            new_name='check1',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='eleven',
            new_name='check10',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='five',
            new_name='check11',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='four',
            new_name='check12',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='nine',
            new_name='check13',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='one',
            new_name='check14',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='seven',
            new_name='check15',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='six',
            new_name='check16',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='ten',
            new_name='check17',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='three',
            new_name='check18',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='twelve',
            new_name='check19',
        ),
        migrations.RenameField(
            model_name='qualities',
            old_name='two',
            new_name='check2',
        ),
        migrations.AddField(
            model_name='qualities',
            name='check20',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check21',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check22',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check23',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check24',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check25',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check3',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check5',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check6',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check7',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check8',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='qualities',
            name='check9',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]

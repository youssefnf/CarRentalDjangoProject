# Generated by Django 4.1.7 on 2023-05-01 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentcarsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voiture',
            name='nb_passager',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='voiture',
            name='nb_portes',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]

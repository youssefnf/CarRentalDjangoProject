# Generated by Django 4.2 on 2023-05-02 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentcarsapp', '0007_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateDebut', models.DateTimeField()),
                ('datefin', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentcarsapp.client')),
                ('voiture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentcarsapp.voiture')),
            ],
        ),
    ]

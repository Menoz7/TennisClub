# Generated by Django 5.1.2 on 2024-11-29 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0005_prenotazione_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='prenotazione',
            name='numero_di_giocatori',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='slotorario',
            name='max_giocatori',
            field=models.IntegerField(default=4),
        ),
    ]

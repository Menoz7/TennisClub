# Generated by Django 5.1.2 on 2024-12-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0006_prenotazione_numero_di_giocatori_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prenotazione',
            name='pagato',
            field=models.BooleanField(default=False),
        ),
    ]
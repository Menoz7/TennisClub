# Generated by Django 5.1.2 on 2024-11-08 15:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0003_campotennis_disponibile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.campotennis')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.slotorario')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
#     
#Modello CampoTennis
class CampoTennis(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    disponibile = models.BooleanField(default=True)
    tipo_superficie = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
#Modello slot orario

class SlotOrario(models.Model):
    data = models.DateField()
    ora_inizio = models.TimeField()
    ora_fine = models.TimeField()
    prenotato = models.BooleanField(default=False)
    campo = models.ForeignKey(CampoTennis, on_delete=models.CASCADE, related_name="slot", null=True)
    max_giocatori = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.data} - {self.ora_inizio} to {self.ora_fine} on {self.campo}"
    

class Prenotazione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    campo = models.ForeignKey(CampoTennis, on_delete=models.CASCADE)
    slot = models.ForeignKey(SlotOrario, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    numero_di_giocatori = models.IntegerField(default=2)
    pagato = models.BooleanField(default=False)

    def __str__(self):
        return f"Prenotazione per {self.utente.username} - {self.campo.nome} - {self.slot}"
    

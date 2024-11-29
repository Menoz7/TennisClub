from django.urls import path
from .views import *
from . import views
#from decorators import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="gestione_home"),
    path('aggiungi/', aggiungi_slot_orario, name='aggiungi_slot_orario'), 
    path('lista/', lista_slot_orari, name="lista_slot_orari"),

    path('aggiungi_slot_automatici/', aggiungi_slot_automatici, name='aggiungi_slot_automatici'),


    #prove varie
    path('prenota_slot/<int:campo_id>', views.prenota_slot_orario, name='prenota_slot_orario'),
    path('riepilogo/<int:prenotazione_id>', views.riepilogo, name='riepilogo')
]
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


    #prenotazione campo e slot orario
    path('prenota_slot/<int:campo_id>', views.prenota_slot_orario, name='prenota_slot_orario'),
    path('riepilogo/<int:prenotazione_id>', views.riepilogo, name='riepilogo'),

    #visualizzare slot orari dell'utente
    path('lista_prenotazioni_utente/', views.ListaPrenotazioniUtente, name='lista_prenotazioni_utente'),
    path('mostra_prenotazione/<int:prenotazione_id>', views.mostra_prenotazione, name='mostra_prenotazione'),
    path('elimina_prenotazione/<int:prenotazione_id>', views.elimina_prenotazione, name="elimina_prenotazione"),
    path('modifica_prenotazione/<int:prenotazione_id>', views.modifica_prenotazione, name='modifica_prenotazione'),
    path('seleziona_slot_modifica/<int:prenotazione_id>/<int:campo_id>/',views.seleziona_slot_modifica, name='seleziona_slot_modifica'),
]
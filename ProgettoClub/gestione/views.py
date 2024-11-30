from django.shortcuts import render, redirect, get_object_or_404

from gestione.utils import crea_slot_orari
from .models import SlotOrario, CampoTennis, Prenotazione
from .forms import SlotOrarioForm, ParametriSlotForm, RicercaDataForm, CampoForm, PrenotazioneForm
from django.contrib import messages
from django.views import View
from django.http import HttpResponse


from datetime import timedelta, datetime
from django.utils import timezone

# Create your views here.

#utilizzo per mostrare i campi si possono prenotare 
def gestione_home(request):
    campi = CampoTennis.objects.filter(disponibile=True) #mostra solo i campi disponibili
    return render(request, 'gestione/gestione_home.html', {'campi': campi})


def lista_slot_orari(request):
    slot_orari = SlotOrario.objects.all().order_by('data', 'ora_inizio')
    return render(request, 'gestione/lista_slot_orari.html', {'slot_orari': slot_orari})

def aggiungi_slot_orario(request):
    if request.method == 'POST':
        form = SlotOrarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_slot_orari')
    else:
        form =SlotOrarioForm()
    return render(request, 'gestione/aggiungi_slot_orario.html', {'form': form})



def aggiungi_slot_automatici(request):
    if request.method == 'POST':
        form = ParametriSlotForm(request.POST)
        if form.is_valid():
            #estrai i dati dal form
            data_inizio = form.cleaned_data['data_inizio']
            data_fine = form.cleaned_data['data_fine']
            ora_inizio = form.cleaned_data['ora_inizio']
            ora_fine = form.cleaned_data['ora_fine']
            durata_slot = form.cleaned_data['durata_slot']


            #richiamo la funzione per creare gli slot orari
            crea_slot_orari(data_inizio, data_fine, ora_inizio, ora_fine, durata_slot)


            #Messaggio di successo
            messages.success(request, "Slot orari creati con successo!")
            return redirect('lista_slot_orari')
    
    else:
        form = ParametriSlotForm()

    return render(request, 'gestione/aggiungi_slot_automatici.html', {'form': form})


###########################
#Prenotazione v.2 con form#
###########################




#nuova versione per creare una prenotazione 
def prenota_slot_orario(request, campo_id):
    campo =get_object_or_404(CampoTennis, id=campo_id)

    #verifica se il campo è disponibile
    if campo.disponibile == False:
        messages.error(request, "Non è possbilile prenotare il campo: MANUTENZIONE")
        return redirect('gestione:gestione_home')

    slot_orari = None
    slot_selezionato = None
    form_prenotazione = None
    form = RicercaDataForm(request.GET)

    if form.is_valid():
        data_cercata = form.cleaned_data['data_cercata']
        print(data_cercata)
        #ricerca time slot 
        slot_orari = SlotOrario.objects.filter(campo=campo, data=data_cercata, prenotato=False)

    if request.method == 'POST':
        print("sono dentro")
        id_slot_orario = request.POST.get('id_slot_orario')
        slot_selezionato = get_object_or_404(SlotOrario, id=id_slot_orario)
        form_prenotazione = PrenotazioneForm(request.POST)

        if form_prenotazione.is_valid() and 'prenota_slot_orario' in request.POST:
            numero_di_giocatori = form_prenotazione.cleaned_data['numero_di_giocatori']
            if numero_di_giocatori <= slot_selezionato.max_giocatori:
                #si crea un record prenotazione
                prenotazione = Prenotazione.objects.create(
                    utente = request.user,
                    campo = slot_selezionato.campo,
                    slot=slot_selezionato,
                    data = timezone.now(), 
                    numero_di_giocatori=numero_di_giocatori
                    )
                prenotazione.save()

                #segno che lo slot è prenotato
                slot_selezionato.prenotato=True
                slot_selezionato.save()

                messages.success(request, f"Prenotazione confermata per {numero_di_giocatori} giocatori dallle {slot_selezionato.ora_inizio}.")

                #ridirezione alla pagina di riepilogo
                return redirect('gestione:riepilogo', prenotazione_id=prenotazione.id)

            

    return render(request, 'gestione/prenota_slot_orario.html', {'form':form, 'slot_orari':slot_orari, 'campo':campo, 'form_prenotazione':form_prenotazione, 'slot_selezionato':slot_selezionato})


#view per visualizare il riepilogo della prenotazione
def riepilogo(request, prenotazione_id):
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)
    return render(request, 'gestione/riepilogo.html',{'prenotazione': prenotazione})


##############################
##Modifica della prenotazione#
##############################

def mostra_prenotazione(request):
    prenotazione = Prenotazione.objects.all()
    return render(request, 'gestione/mostra_prenotazioni.html')


def modifica_prenotazione(request, prenotazione_id):
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)


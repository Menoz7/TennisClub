from django.shortcuts import render, redirect, get_object_or_404

from gestione.utils import crea_slot_orari
from .models import SlotOrario, CampoTennis, Prenotazione
from .forms import SlotOrarioForm,SelezionaCampoForm, ParametriSlotForm, RicercaDataForm, PrenotazioneForm
from django.contrib import messages
from django.views import View
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required


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
@login_required
def prenota_slot_orario(request, campo_id):
    campo = get_object_or_404(CampoTennis, id=campo_id)

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
        form_prenotazione = PrenotazioneForm(request.POST)
        if form_prenotazione.is_valid():
            id_slot_orario = request.POST.get('id_slot_orario')
            print(id_slot_orario)
            slot_selezionato = get_object_or_404(SlotOrario, id=id_slot_orario)
            numero_di_giocatori = int(form_prenotazione.cleaned_data.get('numero_di_giocatori'))
            print(numero_di_giocatori)
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

                messages.success(request, f"Prenotazione confermata per {numero_di_giocatori} giocatori dalle {slot_selezionato.ora_inizio}.")

            #redirezione alla pagina di riepilogo
                return redirect('gestione:riepilogo', prenotazione_id=prenotazione.id)
    else:
        form_prenotazione = PrenotazioneForm()
            

    return render(request, 'gestione/prenota_slot_orario.html', {'form':form, 'slot_orari':slot_orari, 'campo':campo, 'form_prenotazione':form_prenotazione, 'slot_selezionato':slot_selezionato})


#view per visualizare il riepilogo della prenotazione
def riepilogo(request, prenotazione_id):
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)
    return render(request, 'gestione/riepilogo.html',{'prenotazione': prenotazione})


##############################
#lista delle prenotazioni dell'utente
@login_required
def ListaPrenotazioniUtente(request):
    utente_richiesta = request.user
    prenotazioni = Prenotazione.objects.filter(utente=utente_richiesta)
    return render(request, 'gestione/lista_prenotazioni_utente.html', {'prenotazioni': prenotazioni})


##############################
##Modifica della prenotazione#
##############################
@login_required
def mostra_prenotazione(request, prenotazione_id):
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)
    print(prenotazione)
    return render(request, 'gestione/mostra_prenotazione.html', {'prenotazione':prenotazione})


@login_required
def elimina_prenotazione(request, prenotazione_id):
    #recupare prenotazione da cancellare
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)


    if prenotazione.pagato == True:
        messages.error(request, "Non è possibile cancellare una prenotazione già pagata")
        return redirect('gestione:lista_prenotazioni_utente')
    
    if request.method == 'POST':
        #devo ricercare lo slot orario corretto per renderlo di nuovo liber
        slot = get_object_or_404(SlotOrario, id=prenotazione.slot.id)
        slot.prenotato = False
        slot.save()
        #cancella la prenotazione
        prenotazione.delete()
        messages.success(request, "Prenotazione cancellata con successo")
        return redirect('gestione:lista_prenotazioni_utente')
    
    return render(request, "gestione/elimina_prenotazione.html", {'prenotazione': prenotazione})



@login_required
def modifica_prenotazione(request, prenotazione_id):
    if request.method == 'POST':
        form = SelezionaCampoForm(request.POST)
        if form.is_valid():
            nuovo_campo = form.cleaned_data.get('nuovo_campo')
            print(nuovo_campo)

            return redirect('gestione:seleziona_slot_modifica', prenotazione_id=prenotazione_id, campo_id=nuovo_campo.id)
    
    else:
        form = SelezionaCampoForm()

    return render(request, 'gestione/modifica_prenotazione.html', {'form':form, })

@login_required
def seleziona_slot_modifica(request, prenotazione_id, campo_id):

    campo = get_object_or_404(CampoTennis, id=campo_id)
    print(campo)
    #verifica se il campo è disponibile
    if campo.disponibile == False:
        messages.error(request, "Non è possbilile prenotare il campo: MANUTENZIONE")
        return redirect('gestione:gestione_home')
    

    nuovi_slot_orari = None
    nuovo_slot_selezionato = None
    form_prenotazione = None
    form = RicercaDataForm(request.GET)
    if form.is_valid():
        data_cercata = form.cleaned_data['data_cercata']
        print(data_cercata)
            #ricerca time slot 
        nuovi_slot_orari = SlotOrario.objects.filter(campo=campo, data=data_cercata, prenotato=False)    

    if request.method == 'POST':
        form_prenotazione = PrenotazioneForm(request.POST)
        if form_prenotazione.is_valid():
            id_nuovo_slot_orario = request.POST.get('id_slot_orario')
            print(id_nuovo_slot_orario)
            nuovo_slot_selezionato = get_object_or_404(SlotOrario, id=id_nuovo_slot_orario)
            nuovo_numero_di_giocatori = int(form_prenotazione.cleaned_data.get('numero_di_giocatori'))

            vecchia_prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id)

            if nuovo_numero_di_giocatori <= nuovo_slot_selezionato.max_giocatori:
                prenotazione = Prenotazione.objects.create(
                    utente = request.user,
                    campo = nuovo_slot_selezionato.campo,
                    slot = nuovo_slot_selezionato,
                    data = timezone.now(),
                    numero_di_giocatori = nuovo_numero_di_giocatori,
                )
                    
                prenotazione.save()
                nuovo_slot_selezionato.prenotato = True
                nuovo_slot_selezionato.save()

                #modifica della vecchia prenotazione
                vecchia_prenotazione.slot.prenotato=False
                vecchia_prenotazione.slot.save()
                vecchia_prenotazione.delete()


                messages.success(request, f"Prenotazione Modificata con successo per {nuovo_numero_di_giocatori} giocatori dalle {nuovo_slot_selezionato.ora_inizio}")

                return redirect('gestione:riepilogo', prenotazione_id=prenotazione.id)
    else:
        form_prenotazione = PrenotazioneForm()

    return render(request, 'gestione/seleziona_slot_modifica.html', {'form': form,'form_prenotazione': form_prenotazione, 'nuovi_slot_orari':nuovi_slot_orari, 'nuovo_campo':campo})
                    
        
@login_required 
def seleziona_prenotazione(request):
    if request.method == 'POST':
        form_scelta_prenotazione = 
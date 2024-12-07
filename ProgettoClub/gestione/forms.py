from django import forms
from .models import SlotOrario, CampoTennis, Prenotazione

class SlotOrarioForm(forms.ModelForm):
    class Meta:
        model = SlotOrario
        fields = ['data', 'ora_inizio', 'ora_fine', 'prenotato']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora_inizio': forms.TimeInput(attrs={'type': 'time'}),
            'ora_fine': forms.TimeInput(attrs={'type': 'time'}),
        }



class ParametriSlotForm(forms.Form):
    data_inizio = forms.DateField(
        label="Data Inizio",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_fine = forms.DateField(
        label="Data Fine",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    ora_inizio = forms.TimeField(
        label="Ora Inizio",
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    ora_fine = forms.TimeField(
        label="Ora Fine",
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    durata_slot = forms.IntegerField(
        label="Durata Slot (minuti)",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class CampoForm(forms.Form):
    campo = forms.ModelChoiceField(
        queryset=CampoTennis.objects.all(),
        label="Seleziona Campo da tennis",
        widget=forms.Select(attrs={'class': 'form-control'})
    )




class PrenotazioneForm(forms.Form):
    CHOICE_LIST = [(2, "Singolo"), (4, "Doppio")]
    numero_di_giocatori = forms.ChoiceField(label="Numero di giocatori", required=True, choices=CHOICE_LIST)


class RicercaDataForm(forms.Form):
    data_cercata = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Ricerca Data')

class SelezionaCampoForm(forms.Form):
    nuovo_campo = forms.ModelChoiceField(queryset=CampoTennis.objects.all(), empty_label="--Seleziona un campo --", widget=forms.Select(attrs={'class':'form-control'}))


class ModificaPrenotazioneForm(forms.Form):
    campo = forms.ModelChoiceField(queryset=CampoTennis.objects.all(), empty_label="--Seleziona un Campo--", widget=forms.Select(attrs={'class': 'form-control'}))
    data_cercata = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Ricerca Data')

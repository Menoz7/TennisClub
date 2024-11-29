from datetime import datetime, timedelta
from .models import SlotOrario

def crea_slot_orari(data_inizio, data_fine, ora_inizio, ora_fine, durata_slot=30):

    #Crea slot orari tra due date e un intervallo di orari specificato

    #Args:
    # - data_inizio (date): La data inziale per creare gli slot
    # - data_fine (date): La data finale per creare gli slot
    # - ora_inizio (time): L'orario di inzio giornaliero
    # - ora_fine (time): L'orario di fine giornaliero
    # - durata_slot (int): La durata di ciscun slot in minuti


    #conversione ora_inizio e ora_fine in datetime per calcolare facilmente gli slot
    delta_giornaliero = timedelta(days=1)
    durata = timedelta(minutes=durata_slot)
    ora_inizio_dt = datetime.combine(datetime.today(), ora_inizio)
    ora_fine_dt = datetime.combine(datetime.today(), ora_fine)

    #Loop per ogni giorno
    data_corrente = data_inizio
    while data_corrente <= data_fine:
        #loop per ogni intervallo orario
        orario_corrente = ora_inizio_dt
        while orario_corrente + durata <= ora_fine_dt:
            #creo oggetto slot orario
            SlotOrario.objects.create(
                data = data_corrente,
                ora_inizio = orario_corrente.time(),
                ora_fine = (orario_corrente + durata).time(),
                prenotato = False
            )

            #incrementa l'orario corrente con la durata dello slot
            orario_corrente += durata
        
        data_corrente += delta_giornaliero

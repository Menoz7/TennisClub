from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CreaUtente(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            #valore predefinito per il tipo utente membro
            user_type = 'member'

            #Crea o recupera il gruppo in base al tipo di utente
            if user_type=='Membro':
                group, created = Group.objects.get_or_create(name="Membri")
            elif user_type == 'Maestro':
                group, created = Group.objects.get_or_create(name="Maestri")

            #aggiungo utente al gruppo
            group.user_set.add(user)
        
        return user
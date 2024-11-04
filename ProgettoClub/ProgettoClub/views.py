from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import CreaUtente #Utilizza creautente per gestire i vari tipi di utente 
import os
from django.conf import settings
from django.views import View
from django.core.files.storage import FileSystemStorage

# Create your views here.
def project_home(request):
    user = request.user
    context = {
        'is_member': user.groups.filter(name="Member").exists(),
        'is_responsabile': user.groups.filter(name="Responsabile").exists(),
        'is_maestro': user.groups.filter(name="Maestro").exists(),
        'is_superuser':user.is_superuser
    }

    return render(request,'project_home.html',context)


class UserCreateView(CreateView):
    form_class = CreaUtente
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

class ResponsabileCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_responsabile"
    form_class = CreaUtente
    template_name = 'user_create.html'
    success_url = reverse_lazy('gestione_home')

class MaestroCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_maestro"
    form_class = CreaUtente
    template_name = 'user_create.html'
    success_url = reverse_lazy('gestione_home')

class GalleriaFotoView(View):
    def get(self, request, *args, **kwargs):
        # Percorso alla cartella delle foto
        photo_dir = os.path.join(settings.STATICFILES_DIRS[0], 'fotovideo')
        
        # Verifica se la cartella esiste
        if not os.path.exists(photo_dir):
            return render(request, '404.html', status=404)
        
        # Recupera tutti i file immagine nella cartella
        photos = [os.path.join('fotovideo', f) for f in os.listdir(photo_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        return render(request, 'galleria_foto.html', {'photos': photos})
    
def upload_photo(request):
    if request.method == 'POST' and request.user.is_superuser:
        photo = request.FILES['photo']
        fs = FileSystemStorage(location=os.path.join(settings.STATICFILES_DIRS[0], 'fotovideo'))
        filename = fs.save(photo.name, photo)
        return redirect('galleria_foto') 
    return render(request, 'upload_photo.html')  # Sostituisci con il template corretto


def ContactView(request):
    return render(request, template_name='contact.html')

def CampiView(request):
    return render(request, template_name='court.html')

def EventView(request):
    return render(request, template_name='events.html')



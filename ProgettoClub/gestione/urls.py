from django.urls import path
from .views import *
#from decorators import *

app_mame = "gestione"

urlpatterns = [
    path("", gestione_home, name="gestione_home"),
]
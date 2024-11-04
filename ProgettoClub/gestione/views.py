from django.shortcuts import render

# Create your views here.


def gestione_home(request):
    return render(request, gestione_home, 'gestione/gestione_home.html')

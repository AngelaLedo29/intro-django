from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    texto = '''<h1>Librería Local</h1>
    <p>Esta es la página principal de la librería local.</p>'''
    # texto = 'Página inicial de la librería local'
    return HttpResponse(texto)

def acerca_de(request):
    texto = '''<h1>Acerca de</h1>
    <p>Esta es la página acerca de de la librería local.</p>
    <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" alt="Logo de Python" width="500" height="500">'''
    # texto = 'Página acerca de de la librería local'
    return HttpResponse(texto)
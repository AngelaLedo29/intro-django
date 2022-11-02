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
    <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" alt="Logo de Python" width="500" height="500">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/9bZkp7q19f0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
    # texto = 'Página acerca de la librería local'
    return HttpResponse(texto)

def index_general(request):
    texto = '''<h1>Inicio de la Librería Local</h1>
    <p>Esta es la página de inicio de la librería local.</p>
    Si quieres ver el index de la librería local, pulsa <a href="/catalog/">aquí</a>'''
    # texto = 'Página principal de la librería local'
    return HttpResponse(texto)
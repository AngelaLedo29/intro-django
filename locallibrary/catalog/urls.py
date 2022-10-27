# Creamos urls.py en la carpeta catalog
from django.urls import path
from .views import index, acerca_de

urlpatterns = [
    path('', index, name='index'),
    path('acercade/', acerca_de, name='acercade'),
]


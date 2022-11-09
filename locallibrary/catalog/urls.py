# Creamos urls.py en la carpeta catalog
from django.urls import path
from .views import index, acerca_de, BookListView, BookDetailView

urlpatterns = [
    path('', index, name='index'),
    path('acercade/', acerca_de, name='acercade'),
    path('libros/', BookListView.as_view(), name='lista-libros'),
    path('libros/<int:pk>', BookDetailView.as_view(), name='detalle-libro'),
]
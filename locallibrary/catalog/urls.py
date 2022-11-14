# Creamos urls.py en la carpeta catalog
from django.urls import path
from .views import index, acerca_de, BookListView, BookDetailView, AuthorListView, AuthorDetailView, SearchResultsListView, LibrosPrestados, renovar_libro

urlpatterns = [
    path('', index, name='index'),
    path('acercade/', acerca_de, name='acercade'),
    path('libros/', BookListView.as_view(), name='lista-libros'),
    path('libros/<int:pk>', BookDetailView.as_view(), name='detalle-libro'),
    path('autores/', AuthorListView.as_view(), name='lista-autores'),
    path('autores/<int:pk>', AuthorDetailView.as_view(), name='detalle-autor'),
    path('busqueda/', SearchResultsListView.as_view(), name='buscar'),
    path('prestados/', LibrosPrestados.as_view(), name='libros_prestados'),
    path('libro/<uuid:pk>/renovar/', renovar_libro, name='renovar-fecha'),
]
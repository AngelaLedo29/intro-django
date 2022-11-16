# Creamos urls.py en la carpeta catalog
from django.urls import path
from .views import index, acerca_de, BookListView, BookDetailView, AuthorListView, AuthorDetailView, SearchResultsListView, LibrosPrestados, renovar_libro, AuthorCreate, AuthorUpdate, AuthorDelete, BookCreate

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
    path('autor/crear/', AuthorCreate.as_view(), name='crear-autor'),
    path('autor/<int:pk>/actualizar/', AuthorUpdate.as_view(), name='actualizar-autor'),
    path('autor/<int:pk>/eliminar/', AuthorDelete.as_view(), name='eliminar-autor'),
    path('libro/crear/', BookCreate.as_view(), name='crear-libro'),
]
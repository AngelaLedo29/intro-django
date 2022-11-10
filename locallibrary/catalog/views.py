from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Book, BookInstance, Author
from django.views.generic import ListView, DetailView

# Create your views here.
def index_general_old(request):
    texto = '''<h1>Librería Local</h1>
    <p>Esta es la página principal de la librería local.</p>
    <h2>Total de instancias de libros: '''
    texto += f'{Book.objects.all().count()}' '''</h2>'''
    # texto = 'Página inicial de la librería local'
    lista = '<h2>Mi lista de ultimos libros</h2><ul>'
    # Colsulta a la base de datos: primero los 5 libros
    #for libro in Book.objects.all()[:5]:
    #   lista += f'<li>{libro.title} ({libro.author})</li>'
    # Consulta a la base de datos: últimos 5 libros
    for libro in Book.objects.all().order_by('-id')[:5]:
        lista += f'<li>{libro.title}</li>'
    lista += '</ul>' # Fuera del bucle
    # Lista de libros disponibles
    texto += '''<h2>Total de libros disponibles: '''
    libros = BookInstance.objects.filter(status__exact='a').count()
    texto += f'{libros}</h2>'

    return HttpResponse(texto + lista)

def index_general(request):
    return render(request, 'index-general.html')

def acerca_de_old(request):
    texto = '''<h1>Acerca de</h1>
    <p>Esta es la página acerca de de la librería local.</p>
    <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" alt="Logo de Python" width="500" height="500">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/9bZkp7q19f0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
    # texto = 'Página acerca de la librería local'
    return HttpResponse(texto)

def acerca_de(request):
    return render(request, 'acerca-de.html')

def index_old(request):
    texto = '''<h1>Inicio de la Librería Local</h1>
    <p>Esta es la página de inicio de la librería local.</p>
    Si quieres ver el index de la librería local, pulsa <a href="/catalog/">aquí</a>'''
    # texto = 'Página principal de la librería local'
    return HttpResponse(texto)

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    ultimos = Book.objects.all().order_by('-id')[:10]

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_visits':num_visits,
            'ultimos':ultimos},
    )

## Listas Genéricas
class BookListView(ListView):
    '''Vista genérica para el listado de libros'''
    model = Book
    paginate_by = 15
    def get_queryset(self):
        return Book.objects.all().order_by('title')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(DetailView):
    '''Vista genérica para el detalle de un libro'''
    model = Book

class AuthorListView(ListView):
    '''Vista genérica para el listado de autores'''
    model = Author
    paginate_by = 15
    def get_queryset(self):
        return Author.objects.all().order_by('last_name')

class AuthorDetailView(DetailView):
    '''Vista genérica para el detalle de un autor'''
    model = Author

## Busqueda
class SearchResultsListView(ListView):
    model = Book

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        # Voy a guardar Query para el contexto
        self.query = query
        return Book.objects.filter(title__icontains=query)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['query'] = self.query
        return context
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from catalog.models import Book, BookInstance, Author
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail, BadHeaderError

from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm
from catalog.models import Author
from catalog.forms import ContactForm

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
    context = {}
    context['title'] = 'Acerca de'
    context['coords'] = "41.6447242,-0.9231553"

    return render(request, 'acerca_de.html', context)

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
        context['ahora'] = datetime.datetime.now()
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

## Busqueda de libros
class SearchResultsListView(ListView):
    model = Book

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        # Voy a guardar Query para el contexto
        if query:
            self.query = query
            return Book.objects.filter(title__icontains=query)
        else:
            return[]
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['busqueda'] = self.query
        context['anterior'] = self.request.META.get('HTTP_REFERER')
        return context

## Libros prestados
class LibrosPrestados(ListView):
    '''Vista genérica para el listado de libros prestados'''
    model = BookInstance
    template_name = 'catalog/libros_prestados.html'
    paginate_by = 15

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('-due_back')

# Vista para renovar un libro
def renovar_libro(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Si es un POST, procesamos el formulario
    if request.method == 'POST':
        # Creamos un formulario con los datos del POST
        #form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)
    
        # Comprobamos que el formulario es válido
        if form.is_valid():
            # Procesamos los datos del formulario
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.status = form.cleaned_data['status']
            book_instance.save()
    
            # Redirigimos a la página de inicio
            return HttpResponseRedirect(reverse('libros_prestados'))
        
    # Si es un GET, mostramos el formulario
    else:
        # inicializa la fecha de renovación dentro de 3 semanas
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/renovacion_fecha.html', context)

## Gestión de autores con vistas genéricas
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('lista-autores')
    #initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    success_url = reverse_lazy('lista-autores')

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('lista-autores')

## Gestión de libros con vistas genéricas
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    success_url = reverse_lazy('lista-libros')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    success_url = reverse_lazy('lista-libros')

class BookDelete(DeleteView):  
    model = Book
    success_url = reverse_lazy('lista-libros')

## Creación de contacto
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			    'first_name': form.cleaned_data['first_name'], 
			    'last_name': form.cleaned_data['last_name'], 
			    'email': form.cleaned_data['email_address'], 
			    'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("main:homepage")
      
	form = ContactForm()
	return render(request, "acerca_de.html", {'form':form})

## Busqueda de autores
class SearchResultsListViewAuthor(ListView):
    model = Author

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        # Voy a guardar Query para el contexto
        if query:
            self.query = query
            return Author.objects.filter(last_name__icontains=query)
        else:
            return[]
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchResultsListViewAuthor, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['buscar'] = self.query
        context['anterior'] = self.request.META.get('HTTP_REFERER')
        return context
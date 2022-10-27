from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances

# https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Models
# Create your models here.
class Book(models.Model) :
    '''Model reprsenting a book (but not a specific copy of a book).'''
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', 
        on_delete=models.SET_NULL, # que pasa si borramos el autor
        null=True) # puede ser nulo?
    summary = models.TextField(
        max_length=1000, 
        help_text='Enter a brief description of the book',
        blank=True)
    isbn = models.CharField('ISBN', max_length=13, 
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self) :
        '''String for representing the Model object.'''
        return self.title

class Genre(models.Model) :
    '''Model representing a book genre.'''
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self) :
        '''String for representing the Model object.'''
        return self.name

class Language(models.Model) :
    '''Model representing a Language (e.g. English, French, Japanese, etc.)'''
    name = models.CharField(max_length=200, help_text='Enter the book\'s natural language (e.g. English, French, Japanese, etc.)')

    def __str__(self) :
        '''String for representing the Model object.'''
        return self.name
    
class Author(models.Model) :
    """
    Modelo que representa un autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)
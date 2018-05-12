from django.db import models
import uuid
from django.urls import reverse

# Importing the users model
from django.contrib.auth.models import User

from datetime import date

# Create your models here.
# Creating a model for the Genres of books

class Genre(models.Model):
    """
    Model which represents a Genre for a book
    Eg: Fiction, Biography, Non-Fiction etc..
    """

    # Model Fields
    # Since no verbose name has been defined the field will be called Name in forms
    name = models.CharField(max_length=200, help_text="Enter the genre for the book(Fiction, Biography, Non-Fiction)")

    # Model Methods
    def __str__(self):
        """
        Overriding the __str__ method for this class
        The string returned will represent the Gener model in teh admin site
        """
        return self.name

class Language(models.Model):
    """
    Model which represents the language for a book
    """

    language = models.CharField(max_length=200, help_text="Enter the language for the book")

    def __str__(self):
        return self.language


class Book(models.Model):
    """
    Class representing the Book model
    """
    # MODEL FIELDS
    # the title of the book
    title = models.CharField(max_length=200)

    # The summary of the book
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")

    # A foreign key field type is used beacuse a book can have 1 Author
    # but an author can have many books
    # One to Many Field

    # null = True - allows dB to store a NULL value if no author is selected
    # on_delete=models.SET_NULL, which will set the value of the author to Null if the associated author record is deleted.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # The book ISBN
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # The boook genre
    # This is a many-to-many field
    # A bbok may belong to many genres, a genre can have n number of books
    # Note: Genre is the object here
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')


    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    # MODEL METHODS
    def __str__(self):
        """
        Overridden method which represents the model object
        """
        return self.title

    def get_absolute_url(self):
        """
        Reverse mapping of URL.
        Returns a URL to access a detail record for this book
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        A Helper function to return the gener that this book belongs to as a
        string
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """
    Class representing the BookInstance model
    Model representing a specific copy of a book( a book that cna be borrowed from a library)
    """
    # The unique id for the book which will be represented as primary key
    # A unique ID is created for each insatnce of a Book
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    # version details
    version_detail = models.CharField(max_length=200)

    # Due Date to return this book
    due_date = models.DateField(null=True, blank=True)

    # When we use a tuple for displaying a list of choices for the user
    # the value is displayed in teh drop down menu for the user and once the user
    # selects a particluar value, teh corresponding key is stored if teh option
    # is selected
    LOAN_STATUS = (("m", "maintenance"), ("o", "On Loan"), ("a", "Available"), ("r", "reserved"))

    # Creating a choice field which represents teh status of the book
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    # Creating a new field which represents the particular user who has borrowed the book
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Meta data of teh book
    class Meta:
        ordering = ["due_date"]

        permissions = (("can_mark_returned", "Set book as returned"),)


    # MODEL METHODS
    def __str__(self):
        """
        String for representing the Model object
        """
        # Using Python3's string interpolation format
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        """
        Property that lets us know whetehr a book is over due
        Check if due_date is present on this book
        If yes, then check if today's date is greater than the due date
        """
        if self.due_date and date.today() > self.due_date:
            return True
        return False

class Author(models.Model):
    """
    Class represnting the Author model
    """
    # Data representing an author
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Date of Birth
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    # Meta Data for Authors
    class Meta:
        ordering = ["first_name", "last_name"]


    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String represnting and denoting this class
        """
        return f'{self.first_name} {self.last_name}'

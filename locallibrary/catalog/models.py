from django.db import models

# Create your models here.
# Creating a model for the Genres of books

class Genre(models.Model):
    """
    Model which represents a Genre for a book
    Eg: Fiction, Biography, Non-Fiction etc..
    """

    # Model Fields
    # Since no verbose name has been defined the field will be called Name in forms
    name = models.CharField(max_lenght=200, help_text="Enter the genre for the book(Fiction, Biography, Non-Fiction)")

    # Model Methods
    def __str__(self):
        """
        Overriding the __str__ method for this class
        The string returned will represent the Gener model in teh admin site
        """
        return self.name


class Book(models.Model):
    """
    Class representing the Book model
    """
    # MODEL FIELDS
    # the title of the book
    title = models.CharField(max_length=200)

    # The summary of the book
    summary = models.TextField(max_lenght=1000, help_text="Enter a brief description of the book")

    # A foreign key field type is used beacuse a book can have 1 Author
    # but an author can have many books
    # One to Many Field

    # null = True - allows dB to store a NULL value if no author is selected
    # on_delete=models.SET_NULL, which will set the value of the author to Null if the associated author record is deleted.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # The bbok ISBN
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # The boook genre
    # This is a many-to-many field
    # A bbok may belong to many genres, a genre can have n number of books
    # Note: Genre is the object here
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')


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
        return reverse('bbok-detail', args=[str(self.id)])

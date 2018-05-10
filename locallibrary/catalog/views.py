from django.shortcuts import render
from .models import Author, BookInstance, Book, Genre, Language

# Create your views here.
def index(request):
    """
    This is the function taht will be called whenever the user navigates
    to the catalog/ page. This is our site's landing page
    """

    # Get all teh data related to books
    num_books = Book.objects.all().count()

    # Number of book instances
    num_book_instances = BookInstance.objects.all().count()

    # Get a count of all teh available books
    available_books = BookInstance.objects.filter(status__exact="a").count()

    # Get a count of all the authors in teh locallibrary
    num_of_authors = Author.objects.count()

    # The render function takes teh following 3 paramters
    # HttpRequest Object
    # HTMl template with placeholders
    # A dictionary( called context) with the placeholders that will; be placed
     # into the template

    return render(
    request,
    'index.html',
    context={"num_books" : num_books, "num_book_instances": num_book_instances, "available_books": available_books, "num_of_authors" : num_of_authors})

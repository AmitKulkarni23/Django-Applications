from django.shortcuts import render
from .models import Author, BookInstance, Book, Genre, Language
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

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

    # Get the number of counts of visits by a particluar browser
    num_of_visits = request.session.get('num_of_visits', 0)
    request.session["num_of_visits"] = num_of_visits + 1

    # The render function takes teh following 3 paramters
    # HttpRequest Object
    # HTMl template with placeholders
    # A dictionary( called context) with the placeholders that will; be placed
     # into the template

    return render(
    request,
    'index.html',
    context={
    "num_books" : num_books,
    "num_book_instances": num_book_instances,
    "available_books": available_books,
    "num_of_authors" : num_of_authors,
    "num_of_visits" : num_of_visits})


# A class based view( specifically designed for books)
class BookListView(generic.ListView):
    """
    The generic view will query the dB to get all the records
    for the specified model(Book) and render a template located at
    /locallibrary/catalog/templates/catalog/book_list.html

    Within the template you can access the list of books with the template variable
    named object_list or book_list

    """
    model = Book
    paginate_by = 2


# A class based View for Book Details
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_date')

from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language


# Register your models here.

# Creating a Model Admin class for a book instance
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")

# Registering the BookAdmin class along with the actual Book model


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # pass
    list_display = ("book", "id", "status", "due_date")

    # Adding a filter here
    list_filter = ("status", "due_date")
    fieldsets = (
        (None, {
            'fields': ('book','version_detail', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_date','borrower')
        }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "date_of_death")

admin.site.register(Genre)
admin.site.register(Language)

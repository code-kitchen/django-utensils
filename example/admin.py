from django.contrib import admin

from .models import Author, Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_names']


class BookAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'in_stock']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

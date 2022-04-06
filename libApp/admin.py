from django.contrib import admin
from . models import Book

# Register your models here.
class book(admin.ModelAdmin):
    list_display = ['id','name','author','bookId']

admin.site.register(Book,book)
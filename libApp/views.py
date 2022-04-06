from django.shortcuts import render,redirect
from . models import Book
#from django.contrib.auth.models import auth, authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password,check_password

from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == "POST":
        fName = request.POST.get('fName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        if User.objects.filter(username=email).exists():
            messages.success(request,'Email already exists')
            return redirect('/')
        user = User(username=email,password=password,email=email,first_name=fName)
        user.save()
        return redirect('/login')
    return render(request,'libApp/register.html')

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = auth.authenticate(request,username=email,password=password)
        print("=========",user)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages.success(request,'Email or password is Incorrect')
            return redirect('/login')
    return render(request, 'libApp/login.html')


def logoutUser(request):
    logout(request)
    messages.error(request,"Logout")
    return redirect('/')

def home(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(user_id=request.user.id)

        params = {'books':books}
        return render(request,'libApp/home.html',params)
    return redirect('/')

def addBook(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            author = request.POST.get('author')
            bookId = request.POST.get('bookId')
            if Book.objects.filter(bookId=bookId,user=request.user).exists():
                messages.success(request, 'Book Id Already exists')
                return redirect('/home')
            book = Book(name=name, author=author, bookId=bookId, user=request.user)
            book.save()
            return redirect('/home')
        return render(request,'libApp/home.html')

    return redirect('/')

def updateBook(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            author = request.POST.get('author')
            bookId = request.POST.get('bookId')
            book = Book.objects.get(id=id)
            book.name = name
            book.author = author
            book.bookId = bookId
            book.save()
            messages.success(request, 'Book Updated')
            return redirect('/home')
    return redirect('/')

def deleteBook(request,id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, 'Book Deleted')
        return redirect('/home')
    return redirect('/')
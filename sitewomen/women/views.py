from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add article', 'url_name': 'add_page'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': ' Angelina Jolie', 'content': 'Biography of Angelina Jolie', 'is_published': True},
    {'id': 2, 'title': 'Margo Robie', 'content': 'Biography of Margo Robie', 'is_published': False},
    {'id': 3, 'title': 'Julie Roberts', 'content': 'Biography of Julie Roberts', 'is_published': True},
]

class MyClass:
    def __init__(self, a,b):
        self.a = a
        self.b = b

def index(request):
    data = {
        'title': 'Main page',
        'menu': menu,
        'posts': data_db,
            }
    return render(request, "women/index.html", context = data)

def about(request):
    return render(request, "women/about.html", {'title': 'About page'})

def categories(request, cat_id):
    return HttpResponse(f"<h1>Categories</h1><p>id: {cat_id}</p>")

def show_post(request, post_id):
    return HttpResponse(f"displaying an article with id = {post_id}")

def addpage(request):
    return HttpResponse("adding article")
def contact(request):
    return HttpResponse("Feedback")
def login(request):
    return HttpResponse("Authorization")
def page_not_found(request, exception):
    return HttpResponseNotFound("Page not found")
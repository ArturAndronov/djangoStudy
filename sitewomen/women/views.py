from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string

from women.models import Women

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add article', 'url_name': 'add_page'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'}
]

class MyClass:
    def __init__(self, a,b):
        self.a = a
        self.b = b

def index(request):
    posts = Women.published.all()
    data = {
        'title': 'Main page',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
            }
    return render(request, "women/index.html", context = data)

def about(request):
    return render(request, "women/about.html", {'title': 'About page', 'menu': menu})

def categories(request, cat_id):
    return HttpResponse(f"<h1>Categories</h1><p>id: {cat_id}</p>")

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, "women/post.html", data)

def addpage(request):
    return HttpResponse("adding article")
def contact(request):
    return HttpResponse("Feedback")
def login(request):
    return HttpResponse("Authorization")

def show_category(request, cat_id):
    data = {
        'title': 'display by category',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, "women/index.html", context=data)
def page_not_found(request, exception):
    return HttpResponseNotFound("Page not found")
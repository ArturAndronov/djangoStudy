from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, DetailView, FormView
from pip._vendor.rich.markup import Tag

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles
from django.views import View

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add article', 'url_name': 'add_page'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'}
]


class MyClass:
    def __init__(self, a,b):
        self.a = a
        self.b = b

# def index(request):
#     posts = Women.published.all().select_related('cat')
#     data = {
#         'title': 'Main page',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#             }
#     return render(request, "women/index.html", context = data)

class WomenHome(ListView):
   # model = Women
    template_name = 'women/index.html'
    content_object_name = 'posts'
    extra_context = {
        'title': 'Main page',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # < имя приложения > / < имя модели> _list.html
    # women/women_list.html

    # template_name = "women/index.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, "women/about.html",
                  {'title': 'About page', 'menu': menu, 'form': form})

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

class ShowPost(DetailView):
    #model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):
#    if request.method == "POST":
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            #print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect("home")
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#    else:
#        form = AddPostForm()
#
#    data = {
#        'menu': menu,
#        'title': 'Добавление статьи',
#        'form': form
#    }
#    return render(request, "women/addpage.html", data)

class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, "women/addpage.html", data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, "women/addpage.html", data)

def contact(request):
    return HttpResponse("Feedback")
def login(request):
    return HttpResponse("Authorization")

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Heading: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, "women/index.html", context=data)

class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("Page not found")

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f"Tag: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, "women/index.html", context=data)

class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

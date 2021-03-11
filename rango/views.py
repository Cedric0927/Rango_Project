from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rango.forms import CategoryForm
from rango.models import Category, Page


def index(request):
    categories = Category.objects.all()
    print(categories)
    context = {
        "categories": categories
    }
    return render(request, 'rango/index.html', locals())


def show_category(request, slug):
    categories = Category.objects.get(slug=slug)
    print(categories)
    print(type(categories))
    pages = Page.objects.filter(category_id=categories.id)
    context = {
        'categories': categories,
        'pages': pages,
    }
    return render(request, 'rango/context.html', locals())


def add_category(request):
    form = CategoryForm()
    
    if form.method == 'POST':
        form = CategoryForm(request.post)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    context = {
        'form': form
    }

    return render(request, 'rango/add_category.html', locals())
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
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

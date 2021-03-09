from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from rango.models import Category


def index(request):
    category_list = Category.objects.order_by('likes')[:5]
    context = {
        'categories': category_list
    }
    return render(request, 'rango/index.html', context=context)

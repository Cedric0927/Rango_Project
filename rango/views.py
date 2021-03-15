from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.mial import send_verify_email
from rango.models import Category, Page


def first(request):
    send_verify_email()
    return HttpResponseRedirect('/rango/')


def index(request):
    categories = Category.objects.all()
    # return render(request, 'rango/index.html', locals())
    # visitor_cookie_handler(request)
    context = {
        "categories": categories,
        # 'visits': request.session['visits']
    }
    response = render(request, 'rango/index.html', locals())
    # visitor_cookie_handler(request, response)
    return response


@login_required
def show_category(request, slug):
    # categories = Category.objects.get(slug=slug)
    categories = get_object_or_404(Category, slug=slug)
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

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    context = {
        'form': form
    }

    return render(request, 'rango/add_category.html', locals())


def add_page(request, category_slug):
    form = PageForm()
    category = Category.objects.get(slug=category_slug)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            # return index(request)
            return HttpResponse('Add success')
        else:
            print('表单无效')
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'rango/add_page.html', locals())


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm
        profile_form = UserProfileForm

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }

    return render(request, 'rango/register.html', locals())


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')


def visitor_cookie_handler(request, response):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # response.set_cookie('last_visit', str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
        # response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie
    # response.set_cookie('visits', visits)
    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page, BootUser
from rango.send_mail2 import send_mail


def first(request):
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


def bootstrap_register(request):
    if request.method == 'GET':
        context = {
            'title': 'register'
        }
        return render(request, 'boot/register.html', context=context)
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print([user_name, email, password])
        user = BootUser()
        user.user = user_name
        user.email = email
        user.password = password
        user.save()
        # return HttpResponse('注册成功')
        return HttpResponseRedirect('bootstrap_login')
        # return render(request, 'boot/register.html', context={})


def bootstrap_login(request):
    if request.method == 'GET':
        context = {
            'title': 'Login'
        }
        return render(request, 'boot/login.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

    return None


def register3(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            re_password = request.POST.get('re_password')
            user.username = user.email
            user.is_active = False
            validate_password(user.password)
            if re_password == user.password:
                user.set_password(user.password)
                user.save()

                u_token = uuid.uuid4().hex
                print('注册' + str(u_token) + str(user.email))
                cache.set(u_token, user.email, timeout=60 * 10)
                send_mail(user.username, u_token, mail_type='activate')
            else:
                messages.warning(request, 'It is difference between two input')
                # return HttpResponse('Password is wrong')
        else:
            print(user_form.errors)
            return HttpResponse(user_form.errors)
    else:
        user_form = UserForm

    context = {
        'user_form': user_form
    }
    return render(request, 'rango/register3.html', context=context)


def login3(request):
    if request.method == 'POST':
        mail = request.POST.get('email')
        password = request.POST.get('password')
        print([mail, password])
        user = authenticate(username=mail, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # send_mail
                return HttpResponse('Login success')
            else:
                return HttpResponse('Your discount is not activate')
        else:
            return HttpResponse('email or password is wrong')
    else:
        context = {
            'title': "login3"
        }
        return render(request, 'rango/login3.html', context=context)


def send_email(request):
    if request.method == 'POST':
        u_token = uuid.uuid4().hex
        mail = request.POST.get('email')
        send_mail(mail, u_token, mail_type='forget')
        request.session['forget_mail'] = mail
        return HttpResponse('Mail has sent')
    else:
        return render(request, 'find_password/forget.html')


def activate(request):
    if request.method == 'POST':
        u_token = request.GET.get('u_token')
        print(u_token)
        user_email = cache.get(u_token)
        print(user_email)
        user = User.objects.get(email=user_email)
        user.is_active = True
        user.save()
        return HttpResponse('Activate success')
    else:
        return render(request, 'find_password/new_password.html')


def change_password(request):
    # if request.method == 'POST':
    username = request.session.get('_auth_user_id')
    if username:
        user = User.objects.get(pk=username)
        user.set_password('12345')
        user.save()
    return HttpResponse('Change success')


def set_cookie(request):
    # response = HttpResponse('')
    # # user = response.set_cookie('username', 'cedric')
    # user = response.get('username')
    # response.set_signed_cookie('content', user, '1234')
    request.session['username'] = 'cedic'
    return HttpResponse('Session add success')


def get_cookie(request):
    # user = request.session.get('username')
    # return HttpResponse(user)
    return HttpResponseRedirect('/rango/login3/')


def forget_password(request):
    if request.method == 'POST':
        mail = request.session.get('forget_mail')
        print(mail)
        user = User.objects.get(email=mail)
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect('/rango/login3/')
    else:
        return render(request, 'find_password/new_password.html')


def test(request):

    return HttpResponse('<ul class="errorlist"><li>username<ul class="errorlist"><li>A user with that username already exists.</li></ul></li></ul>')
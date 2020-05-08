# from django.contrib.auth.decorators import 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from .models import User


def login_user(request):
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = username = form.cleaned_data['email_or_id']
            pwd = form.cleaned_data['password']

            user = authenticate(request, email=email, username=username, password=pwd)

            if user is not None:
                login(request, user)
                return redirect('main:index')
            else:
                context['error'] = True

        else:
            context['error'] = True
    else:
        form = LoginForm()
    
    context['form'] = form

    return render(request, 'useraccount/login.html', context)


def register(request):
    context = {}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:

            if form.is_valid():
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    civility=form.cleaned_data['civility'],
                    phone_number=form.cleaned_data['phone_number'],
                    adress=form.cleaned_data['adress'],
                    postal_code=form.cleaned_data['postal_code'],
                    city=form.cleaned_data['city'],
                )
                user.save()
                return redirect('main:index')

            else:
                context['error'] = 'formulaire non valide'

        else:
            context['error'] = 'mot de passe non identique'

    else:
        form = RegisterForm()

    context['form'] = form

    return render(request, 'useraccount/register.html', context)

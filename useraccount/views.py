# from django.contrib.auth.decorators import 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm


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

    context['form'] = RegisterForm()

    return render(request, 'useraccount/register.html', context)

from django.http import JsonResponse 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from senderemail.register import sender_activate_account
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
                user.generate_activate_key()
                sender_activate_account(user, request.get_host())

                return redirect('main:index')

            else:
                context['error'] = 'formulaire non valide'

        else:
            context['error'] = 'mot de passe non identique'

    else:
        form = RegisterForm()

    context['form'] = form

    return render(request, 'useraccount/register.html', context)

@login_required
def account(request):
    return render(request, 'useraccount/account.html')

@login_required
def change_pwd(request):
    if request.method == 'POST':
        user = request.user
        try:
            user.set_password(request.POST['new_pwd'])
            user.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})

    else:
        return redirect('useraccount:account')

@login_required
def change_user_infos(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST

        try:
            user.first_name = data['id_first_name']
            user.last_name = data['id_last_name']
            user.username = data['id_pseudo']
            user.email = data['id_email']
            user.phone_number = data['id_phone_number']
            user.adress = data['id_adress']
            user.postal_code = data['id_postal_code']
            user.city = data['id_city'].upper()
            user.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})

    else:
        return redirect('useraccount:account')

def active_account(request):
    context = {}
    id_user = request.GET['id']
    key = request.GET['key']
    user = User.objects.get(pk=id_user)

    if user.activate_key == key:
        user.is_verified = True
        user.save()
        context['is_validate'] = True

    else:
        context['is_validate'] = False

    return render(request, 'useraccount/activated.html', context)
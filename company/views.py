from django.shortcuts import render
from django.shortcuts import redirect
from company.forms import *
from company.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    return render(request, 'company_templates/index.html')


def signUp(request):
    return render(request, 'company_templates/signup.html')

def logIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Algo salio mal, revisa bien los datos ingresados.')
    return render(request, 'company_templates/login.html',{
        'login':login,
    })

def logOut(request):
    logout(request)
    return redirect('/')


def createAccount(request):

    register_form = formAccount()
    if request.method == 'POST':
        register_form = formAccount(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('ingreso')

    return render(request, 'company_templates/create-account.html',{
        'register_form' : register_form
    })

def dashboard(request):
    user = request.user.id
    bussines = ProfileBussines.objects.filter(user=1).count()
    return render(request, 'company_templates/dashboard.html',{
        bussines : 'bussines'
    })

def bussines(request):

    users = request.user.id
    user = User.objects.get(id=users)

    if request.method == 'POST':
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data

            # Datos
            name = data_form.get('name')
            category = data_form.get('category')
            photo_portada = data_form.get('photo_portada')
            photo_profile = data_form.get('photo_profile')
            description = data_form.get('description')
            email = data_form.get('email')
            contact = data_form.get('contact')
            facebook = data_form.get('facebook')
            instagram = data_form.get('instagram')
            whatsapp = data_form.get('whatsapp')

            bussines = ProfileBussines(
                user_id = users,
                name = name,
                category = category,
                photo_portada = photo_portada,
                photo_profile = photo_profile,
                description = description,
                email = email,
                contact = contact,
                facebook = facebook,
                instagram = instagram,
                whatsapp = whatsapp,
            )
            bussines.save()
            
            messages.success(request, 'Tu negocio ha sido guardado con exito!')
            return redirect('bussines')
        else:
            messages.error(request, 'Algo ha ocurrido, revisa bien tus datos')
    else:
        form = Form()

    return render(request, 'company_templates/profile_bussines.html', {
        'form': form
    })
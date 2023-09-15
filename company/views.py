from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from company.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
# Create your views here.


def index(request, name):
    username = User.objects.get(username=request.user.username)  
    return render(request, 'company_templates/index.html',{
        'username' : username
    })

def home(request):
    return render(request, 'company_templates/index.html',{
    })

def signUp(request):
    return render(request, 'company_templates/signup.html')

def logIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(f'index', request.user.username)
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

def dashboard(request, name):
    username = User.objects.get(username=name)
    user = request.user.id
    bussines = ProfileBussines.objects.filter(user_id=user).count()
    profile = ProfileBussines.objects.all()

    return render(request, 'company_templates/dashboard.html',{
        'bussines' : bussines,
        'username' : username,
        'profile' : profile ,
    })



def bussines(request):
    username = User.objects.get(username=request.user.username)
    users = request.user.id

    if request.method == 'POST':
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data

            # Datos
            name = data_form.get('name')
            bio = data_form.get('bio')
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
                bio = bio,
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
        'form': form,
        'username': username
    })


def profile(request, name, id):
    username = User.objects.get(username=request.user.username)
    perfil = ProfileBussines.objects.get(name=name)
    idperfil = perfil.id
    

    # Articulos
    catalogos = Catalogos.objects.filter(profile=id)
    # Paginar Articulos
    paginator_articulos = Paginator(catalogos, 3)
    # Recoger numero pagina
    page_number = request.GET.get('page')
    page_obj = paginator_articulos.get_page(page_number)

    return render(request, 'company_templates/profile.html', {
        'perfil':perfil,
        'username' : username,
        'catalogos' : catalogos,
        'page_catalogos' : page_obj
    })


def editionProfile(request, id):
    username = User.objects.get(username=request.user.username)
    perfil = ProfileBussines.objects.get(id=id)
    urlCurrently = request.META.get('HTTP_REFERER') # Here

    form = eForm(request.POST, request.FILES, instance=perfil)
    if form.is_valid():
        form.save()
        messages.success(request, f'Se ha modificado tu perfil con exito! Deseas ver tu perfil {perfil.name}?')
        return redirect(urlCurrently)
        #return redirect('perfil',perfil.name)
    else:
        return render(request, 'company_templates/edit-profile.html', {
            'perfil' : perfil,
            'form' : form,
            'username' : username
        })
    
def viewCatalog(request):
    username = User.objects.get(username=request.user.username)
    catalogos = Catalogos.objects.filter(user=request.user.id)

    # Paginar Catalogos
    paginator = Paginator(catalogos, 3)
    # Recoger numero pagina
    page = request.GET.get('page')
    page_catalogos = paginator.get_page(page)

    return render(request, 'company_templates/crud-catalogo/edit-catalog.html', {
        'catalogos' : page_catalogos,
        'username' : username,
    })


def editCatalog(request, id):
    username = User.objects.get(username=request.user.username)
    catalogos = Catalogos.objects.get(id=id)
    urlCurrently = request.META.get('HTTP_REFERER')
    form = editCatalogoForm(request.POST, request.FILES, instance=catalogos)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'El catalogo ha sido editado con exito!')
            return redirect(urlCurrently)
        else:  
            messages.error(request, 'No se pudo editar el catalogo.')
            return redirect(urlCurrently)
    else:
        return render(request, 'company_templates/crud-catalogo/update-catalog.html', {
            'username' : username,
            'catalogo' : catalogos,
            'form' : form
    })


def deleteCatalog(request, id):
        catalogo = Catalogos.objects.get(id=id)
        urlCurrently = request.META.get('HTTP_REFERER')
        catalogo.delete()
        return redirect(urlCurrently)

def selectCatalog(request):
    user = request.user.id
    perfilId = ProfileBussines.objects.filter(user_id=user)
    username = User.objects.get(username=request.user.username)

    # Articulos
    perfil = ProfileBussines.objects.filter(user_id=user)
    # Paginar Articulos
    paginator_perfiles = Paginator(perfilId, 3)
    # Recoger numero pagina
    page_number = request.GET.get('page')
    page_obj = paginator_perfiles.get_page(page_number)

    return render(request, 'company_templates/crud-catalogo/select-profile.html', {
        'perfiles' : perfil,
        'page_perfiles' : page_obj,
        'username': username
    })

def addCatalog(request, id):
    user = request.user.id
    username = User.objects.get(username=request.user.username)
    urlCurrently = request.META.get('HTTP_REFERER') # Here
    if request.method == 'POST':
        form = catalogForm(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data

            # Datos
            name = data_form.get('name')
            description= data_form.get('description')
            photo_portada = data_form.get('photo_portada')
            catalog = Catalogos(
                user_id = user,
                profile_id = id,
                name = name,
                photo_portada = photo_portada,
                description = description
            )
            catalog.save()
            messages.success(request, 'Tu catalogo a sido guardado correctamente! ')
            return redirect(f'addCatalogo', id)
        else:
            messages.error(request, 'No se pudo guardar tu catalogo, revisa la informacion ingresada')
            #return redirect(urlCurrently)
    else:
        form = catalogForm()   
    return render(request, 'company_templates/crud-catalogo/add-catalogo.html', {
        'form': form,
        'username': username
    })
    

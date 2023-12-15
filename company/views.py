from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from company.models import *
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
import random
import secrets
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.

def generar_codigo_unico(length=10):
    """
    Genera un código único aleatorio.
    
    Parameters:
    - length (int): Longitud del código único (por defecto, 10).

    Returns:
    - str: Código único generado.
    """
    return secrets.token_hex(length // 2)

# Ejemplo de uso
codigo_unico = generar_codigo_unico()
print(codigo_unico)

def generar_url(request):
    # Reemplaza 'nombre_de_vista' con el nombre de la vista para la cual deseas generar la URL
    url_generada = reverse('perfil', args=[request.user.username, request.user.id])  # Puedes pasar argumentos según sea necesario
    data = {'url_generada': request.build_absolute_uri(url_generada)}
    return JsonResponse(data)

def url_catalogo(request):
    
    url_catalogo = reverse('catalogo', args=[])  # Puedes pasar argumentos según sea necesario
    data = {'url_catalogo': request.build_absolute_uri(url_catalogo)}
    return JsonResponse(data)


def index(request, name):
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = 'Perfil de usuario incorrecto'   
    username = User.objects.get(username=request.user.username)  
    return render(request, 'company_templates/index.html',{
        'username' : username,
        'perfilAccount' : perfilAccount,
    })

def layout(request):
    perfilAccount = Account.objects.get(user_id=request.user.id)
    return render (request, 'company_templates/layouts/layout.html', {
        'perfilAccount' : perfilAccount,
    })

def home(request):
    try:
        username = User.objects.get(username=request.user.username) 
    except User.DoesNotExist:
        username = None

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    return render(request, 'company_templates/index.html',{
        'username' : username,
        'perfilAccount' : perfilAccount,
    })

def signUp(request):
    return render(request, 'company_templates/signup.html')

def logIn(request):
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

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
    cant_catalog = Catalogos.objects.filter(user_id=user).count()
    bussines = ProfileBussines.objects.filter(user_id=user).count()
    profile = ProfileBussines.objects.all()
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    return render(request, 'company_templates/dashboard.html',{
        'bussines' : bussines,
        'cant_catalog' : cant_catalog,
        'username' : username,
        'profile' : profile ,
        'perfilAccount' : perfilAccount ,
    })



def bussines(request):
    username = User.objects.get(username=request.user.username)
    users = request.user.id
    try: 
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

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
        'username': username,
        'perfilAccount' : perfilAccount,
    })


def profile(request, name, id):
    username = User.objects.get(username=request.user.username)
    perfilBusiness = ProfileBussines.objects.get(name=name)
    idperfil = perfilBusiness.id
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    # Contador de productos y servicios de catalogos
    cant_catalogs = Catalogos.objects.annotate(cantPro = models.Count('product'))
    cant_services = Catalogos.objects.annotate(cantSer = models.Count('service'))

    # Articulos
    catalogos = Catalogos.objects.filter(profile=id)
    # Paginar Articulos
    paginator_articulos = Paginator(catalogos, 3)
    # Recoger numero pagina
    page_number = request.GET.get('page')
    page_obj = paginator_articulos.get_page(page_number)

    return render(request, 'company_templates/profile.html', {
        'perfilBusiness':perfilBusiness,
        'username' : username,
        'cant_catalogs' : cant_catalogs,
        'cant_services' : cant_services,
        'catalogos' : catalogos,
        'page_catalogos' : page_obj,
        'perfilAccount' : perfilAccount,
    })


def editionProfile(request, id):
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    username = User.objects.get(username=request.user.username)
    perfilBusiness = ProfileBussines.objects.get(id=id)
    urlCurrently = request.META.get('HTTP_REFERER') # Here

    form = eForm(request.POST, request.FILES, instance=perfilBusiness)
    if form.is_valid():
        form.save()
        messages.success(request, f'Se ha modificado tu perfil con exito! Deseas ver tu perfil {perfil.name}?')
        return redirect(urlCurrently)
        #return redirect('perfil',perfil.name)
    else:
        return render(request, 'company_templates/edit-profile.html', {
            'perfil' : perfilBusiness,
            'form' : form,
            'username' : username,
            'perfilAccount' : perfilAccount,
        })
    
def viewCatalogUser(request, name, id):
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    username = User.objects.get(username=request.user.username)
    catalogos = Catalogos.objects.filter(user=request.user.id)
    cant_catalogs = Catalogos.objects.annotate(cantPro = models.Count('product'))
    cant_services = Catalogos.objects.annotate(cantSer = models.Count('service'))

    # Paginar Catalogos
    paginator = Paginator(catalogos, 3)
    # Recoger numero pagina
    page = request.GET.get('page')
    page_catalogos = paginator.get_page(page)

    return render(request, 'company_templates/crud-catalogo/edit-catalog.html', {
        'catalogos' : page_catalogos,
        'username' : username,
        'perfilAccount' : perfilAccount,
        'cant_catalogs' : cant_catalogs,
        'cant_services' : cant_services,
    })


def editCatalog(request, id):
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

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
            'perfilAccount' : perfilAccount,
            'catalogo' : catalogos,
            'form' : form
    })


def deleteCatalog(request, id):
        catalogo = Catalogos.objects.get(id=id)
        urlCurrently = request.META.get('HTTP_REFERER')
        catalogo.delete()
        return redirect(urlCurrently)

def selectCatalog(request):

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    user = request.user.id
    perfilId = ProfileBussines.objects.filter(user_id=user)
    username = User.objects.get(username=request.user.username)

    # Catalogos
    perfil = ProfileBussines.objects.filter(user_id=user)
    # Paginar Catalogos
    paginator_perfiles = Paginator(perfilId, 3)
    # Recoger numero pagina
    page_number = request.GET.get('page')
    page_obj = paginator_perfiles.get_page(page_number)

    return render(request, 'company_templates/crud-catalogo/select-profile.html', {
        'perfiles' : perfil,
        'page_perfiles' : page_obj,
        'username': username,
        'perfilAccount' : perfilAccount,
    })

def addCatalog(request, id):
    
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    user = request.user.id
    username = User.objects.get(username=request.user.username)
    urlCurrently = request.META.get('HTTP_REFERER') # Here
    if request.method == 'POST':
        form = catalogForm(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data

            # Datos
            name = data_form.get('name')
            category = data_form.get('category')
            type_catalog = data_form.get('type_catalog')
            description= data_form.get('description')
            photo_portada = data_form.get('photo_portada')
            catalog = Catalogos(
                user_id = user,
                category = category,
                type_catalog = type_catalog,
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
        'username': username,
        'perfilAccount' : perfilAccount,
    })
    


def viewProduct(request, name, id):
    username = User.objects.get(username=request.user.username)
    query = request.GET.get('buscar','')
    filter_catalog = request.GET.get('catalog')
    filter_category = request.GET.get('category')

    urlCurrently = request.META.get('HTTP_REFERER')
    try:
        productos = Products.objects.filter(user=id)
    except Products.DoesNotExist:
        productos = None

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None
    
    # Filtro por categorias
    category = Category.objects.filter(type_categorie='Productos')

    # Filtro por catalogos
    catalogs = Catalogos.objects.filter(type_catalog='Productos',user_id=request.user.id)

    if query:
        # Utilizamos Q objects para realizar una búsqueda OR entre campos
        productos = Products.objects.filter(
            Q(name_product__icontains=query) | Q(description__icontains=query) | Q(id_product__icontains=query),
            # Agrega más campos según tus necesidades
        )

    if filter_catalog:
        productos = Products.objects.filter(
            Q(name_product__icontains=query) | Q(description__icontains=query) | Q(id_product__icontains=query),
            Q(catalog_id__name__icontains=filter_catalog)
        )
    
    if filter_category:
        productos = Products.objects.filter(
            Q(name_product__icontains=query) | Q(description__icontains=query) | Q(id_product__icontains=query),
            Q(catalog_id__name__icontains=filter_catalog),
            Q(category_id__name__icontains=filter_category)
        )
    

    return render(request, 'company_templates/crud-productos/view-product.html', {
    'username':username,
    'productos':productos,
    'filter_catalog':filter_catalog,
    'filter_category':filter_category,
    'query':query,
    'category':category,
    'catalogs':catalogs,
    'url':urlCurrently,
    'perfilAccount' : perfilAccount,
    })

def editProduct(request, name, id):
    username = User.objects.get(username=request.user.username)
    idproduct = request.user.id

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    try:
        producto = Products.objects.get(id=id)
        form = productEditForm(request.POST, request.FILES, instance=producto)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'El producto ha sido editado con exito.')
                return redirect(f'productos', username, idproduct)
            else:
                messages.error(request, 'El producto no se pudo editar revisa los datos.')
        
    except Products.DoesNotExist:
        producto = None
    
    return render(request, 'company_templates/crud-productos/edit-product.html', {
        'username' : username,
        'producto' : producto,
        'form' : form,
        'perfilAccount' : perfilAccount,
    })

def addProduct(request, name, id):
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None
    
    username = User.objects.get(username=request.user.username)
    number_random = random.randint(10000, 99999)
    urlCurrently = request.META.get('HTTP_REFERER') 
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data
            profile = data_form.get('profile')
            catalog = data_form.get('catalog_id')
            name_product = data_form.get('name_product')
            color = data_form.get('color')
            brand = data_form.get('brand')
            category = data_form.get('category_id')
            quantities = data_form.get('quantities')
            price = data_form.get('price')
            description = data_form.get('description')
            photo_product1 = data_form.get('photo_product1')
            photo_product2 = data_form.get('photo_product2')
            photo_product3 = data_form.get('photo_product3')
            photo_product4 = data_form.get('photo_product4')
            
            
            product = Products(
            
                id_product = number_random,
                user_id = request.user.id,
                catalog = catalog,
                profile = profile,
                name_product = name_product,
                category = category,
                color = color,
                brand = brand,
                quantities = quantities,
                description = description,
                price = price,
                photo_product1 = photo_product1,
                photo_product2 = photo_product2,
                photo_product3 = photo_product3,
                photo_product4 = photo_product4
            )

            product.save()
            messages.success(request, 'El producto fue guardado con exito.')
            return redirect(urlCurrently)
        else:
            messages.error(request, 'Error, el producto no fue guardado, revisa tus datos.')
    else:
        form = productForm()
    return render(request, 'company_templates/crud-productos/add-product.html', {
        'form' : form,
        'perfilAccount' : perfilAccount,
        'username' : username,
    })

def deleteProduct(request, id):
    producto = Products.objects.get(id=id)
    urlcurrently = request.META.get('HTTP_REFERER')
    producto.delete()
    messages.success(request, 'Producto eliminado con exito.')
    return redirect(urlcurrently)



def viewService(request, name, id):
    query = request.GET.get('buscar','')
    filter_catalog = request.GET.get('catalog')
    filter_category = request.GET.get('category')

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    username = User.objects.get(username=request.user.username)
    try: 
        servicio = Services.objects.filter(user_id=id)
    except Services.DoesNotExist:
        servicio = None

    # Filtro por categorias
    category = Category.objects.filter(type_categorie='Servicios')

    # Filtro por catalogos
    catalogs = Catalogos.objects.filter(type_catalog='Servicios',user_id=request.user.id)

    if query:
        # Utilizamos Q objects para realizar una búsqueda OR entre campos
        servicio = Services.objects.filter(
            Q(name_service__icontains=query) | Q(description__icontains=query) | Q(id_service__icontains=query),
            # Agrega más campos según tus necesidades
        )

    if filter_catalog:
        servicio = Services.objects.filter(
            Q(name_service__icontains=query) | Q(description__icontains=query) | Q(id_service__icontains=query),
            Q(catalog_id__name__icontains=filter_catalog)
        )
    
    if filter_category:
        servicio = Services.objects.filter(
            Q(name_service__icontains=query) | Q(description__icontains=query) | Q(id_service__icontains=query),
            Q(catalog_id__name__icontains=filter_catalog),
            Q(category_id__name__icontains=filter_category)
        )

    return render(request, 'company_templates/crud-servicios/view-services.html',{
        'servicios' : servicio,
        'username' : username,
        'perfilAccount' : perfilAccount,
        'filter_catalog':filter_catalog,
        'filter_category':filter_category,
        'query':query,
        'category':category,
        'catalogs':catalogs,
    })


def addService(request, name, id):

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    username = User.objects.get(username=request.user.username)
    number_random = random.randint(10000, 99999)
    urlCurrently = request.META.get('HTTP_REFERER') 
    if request.method == 'POST':
        form = serviceForm(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data
            profile = data_form.get('profile')
            catalog = data_form.get('catalog')
            name_service = data_form.get('name_service')
            category = data_form.get('category')
            price = data_form.get('price')
            photo_service1 = data_form.get('photo_service1')
            photo_service2 = data_form.get('photo_service2')
            photo_service3 = data_form.get('photo_service3')
            photo_service4 = data_form.get('photo_service4')


            service = Services(
                id_service = number_random,
                user_id = request.user.id,
                catalog = catalog,
                profile = profile,
                name_service = name_service,
                category = category,
                price = price,
                photo_service1 = photo_service1,
                photo_service2 = photo_service2,
                photo_service3 = photo_service3,
                photo_service4 = photo_service4
            )

            service.save()
            messages.success(request, 'El servicio fue guardado con exito.')
            return redirect(urlCurrently)
        else:
            messages.error(request, 'Error, el servicio no fue guardado, revisa tus datos.')
    else:
        form = serviceForm()
    return render(request, 'company_templates/crud-servicios/add-service.html', {
        'form' : form,
        'perfilAccount' : perfilAccount,
        'username' : username,
    })

def editService(request, name, id):
    username = User.objects.get(username=request.user.username)
    idservicio = request.user.id

    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    try:
        servicio = Services.objects.get(id=id)
        form = serviceEditForm(request.POST, request.FILES, instance=servicio)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'El servicio ha sido editado con exito.')
                return redirect(f'productos', username, idservicio)
            else:
                messages.error(request, 'El servicio no se pudo editar revisa los datos.')
        
    except Services.DoesNotExist:
        servicio = None
    
    return render(request, 'company_templates/crud-servicios/edit-service.html', {
        'username' : username,
        'servicio' : servicio,
        'form' : form,
        'perfilAccount' : perfilAccount,
    })
    

def view_profile(request, name, id):
    username = User.objects.get(username=request.user.username)
    urlCurrently = request.META.get('HTTP_REFERER')
    
    try:
        profileBusiness = ProfileBussines.objects.filter(user_id=id)
    except ProfileBussines.DoesNotExist:
        profileBusiness = None

    try:
        perfilAccount = Account.objects.get(user_id=id)
    except Account.DoesNotExist:
        perfilAccount = None

    if request.method == 'POST':
        form = perfilUsuer(request.POST, request.FILES)
        if form.is_valid():
           data_form = form.cleaned_data
           birthday = data_form.get('birthday')
           photo_profile = data_form.get('photo_profile')
           country = data_form.get('country')
           city = data_form.get('city')
           bio = data_form.get('bio')
           email = data_form.get('email')
           facebook = data_form.get('facebook')
           instagram = data_form.get('instagram')
           whatsapp = data_form.get('whatsapp')
           indicative = data_form.get('indicative')
           contact = data_form.get('contact')
           gender = data_form.get('gender')

           dates = Account(
               user_id = request.user.id,
               photo_profile = photo_profile,
               birthday = birthday,
               country = country,
               city = city,
               indicative = indicative,
               contact = contact,
               bio = bio,
               email = email,
               facebook = facebook,
               instagram = instagram,
               whatsapp = whatsapp,
               gender = gender,
           )

           dates.save()
           messages.success(request, 'Se ha guardado el perfil personal de tu cuenta')
           return redirect(urlCurrently)
        else:
            messages.error(request, 'Lo sentimos no hemos podido guardar la informacion de tu perfil')
    else:
        form = perfilUsuer()   

    return render(request, 'company_templates/profile-user/show-profile.html', {
       'username' : username, 
       'form' : form,
       'profile' : profileBusiness,
       'perfilAccount' : perfilAccount,
    })

def viewCatalog(request, name_profile, name, id):
    urlCurrently = request.get_full_path()
    busqueda = request.GET.get("buscar")
    color = request.GET.get("color")
    filCategory = request.GET.get("category")

    try:
        profileBusiness = ProfileBussines.objects.get(name=name_profile)
    except ProfileBussines.DoesNotExist:
        profileBusiness = None

    username = User.objects.get(username=request.user.username)
    try:
        perfilAccount = Account.objects.get(user_id=request.user.id)
    except Account.DoesNotExist:
        perfilAccount = None

    try:
        productos = Products.objects.filter(catalog_id=id)
    except Products.DoesNotExist:
        productos = None

    try:
        servicios = Services.objects.filter(catalog_id=id)
    except Products.DoesNotExist:
        servicios = None

    # url 

    if busqueda :
        productos = Products.objects.filter(
            Q(name_product__icontains = busqueda)
        ).distinct()

    if color :
        productos = Products.objects.filter(
            Q(name_product__icontains = busqueda),
            Q(color__icontains = color)
        ).distinct()

    if filCategory:
        productos = Products.objects.filter(
            Q(category_id__icontains = filCategory)
        ).distinct()
    
    # Filtro de catalogos
    filterCatalog = Catalogos.objects.filter(profile_id=request.user.id, type_catalog='Productos')

    # Filtro de Categorias
    filterCategory = Category.objects.filter(type_categorie='Producto')


    catalogo = Catalogos.objects.get(id=id)

    return render(request, 'company_templates/crud-catalogo/view-catalog.html', {
        'catalogo' : catalogo,
        'urlCurrently' : urlCurrently,
        'profileBusiness' : profileBusiness,
        'filterCategories' : filterCategory,
        'filtroCatalogos' : filterCatalog,
        'username' : username, 
        'productos' : productos,
        'servicios' : servicios,
        'perfilAccount' : perfilAccount,
    })

def acercaDe (request):
    return render(request, 'company_templates/acerca-de/index.html',{
    })
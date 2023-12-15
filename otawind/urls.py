
from django.contrib import admin
from django.urls import include, path
from company import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404

urlpatterns = [
    path('generar_url/', views.generar_url, name="generar_url"),
    path('url_catalogo/', views.generar_url, name="url_catalogo"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name="home"),
    path('home/<str:name>', views.index, name="index"),
    path("registro", views.signUp, name="registro"),
    path("accounts/login/", views.logIn, name="ingreso"),
    path('logout/', views.logOut, name="logout"),
    path('creacion/', views.createAccount, name="creacion"),
    path('dashboard/<str:name>/',login_required(views.dashboard), name="dashboard"),
    path('bussines-profile/',login_required(views.bussines), name="bussines"),
    path('perfil/<str:name>/<int:id>',login_required(views.profile), name="perfil"),
    path('edicion-perfil/<int:id>',login_required(views.editionProfile), name="edicionPerfil"),
    path('seleccionar-perfil',login_required(views.selectCatalog), name="selectPerfil"),
    path('agregar-catalogo/<int:id>',login_required(views.addCatalog), name="addCatalogo"),
    path('ver-catalogo/<str:name>/<int:id>', login_required(views.viewCatalogUser), name="viewCatalogo"),
    path('edicion-catalogo/<int:id>', login_required(views.editCatalog), name="edicionCatalogo"),
    path('eliminar-catalogo/<int:id>', login_required(views.deleteCatalog), name="eliminarCatalogo"),
    path('productos/<str:name>/<int:id>', login_required(views.viewProduct), name="productos"),
    path('agregar-producto/<str:name>/<int:id>', login_required(views.addProduct), name="addProductos"),
    path('editar-producto/<str:name>/<int:id>', login_required(views.editProduct), name="edicionProducto"),
    path('eliminar-producto/<int:id>', login_required(views.deleteProduct), name="eliminarProducto"),
    path('servicios/<str:name>/<int:id>', login_required(views.viewService), name="servicios"),
    path('agregar-servicio/<str:name>/<int:id>', login_required(views.addService), name="addServicios"),
    path('editar-servicio/<str:name>/<int:id>', login_required(views.editService), name="edicionServicio"),
    path('perfil-usuario/<str:name>/<int:id>', login_required(views.view_profile), name="viewPerfil"),
    path('catalogo/<str:name_profile>/<str:name>/<int:id>', views.viewCatalog, name="verCatalogo"),
    path('acerca-de-otawind/', views.acercaDe, name="acercaDe"),
]



# cONFIGURACION PARA CARGAR IMAGENES
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

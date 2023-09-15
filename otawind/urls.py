
from django.contrib import admin
from django.urls import path
from company import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('home/<str:name>', views.index, name="index"),
    path("registro", views.signUp, name="registro"),
    path("accounts/login/", views.logIn, name="ingreso"),
    path('logout/', views.logOut, name="logout"),
    path('creacion/', views.createAccount, name="creacion"),
    path('dashboard/<str:name>',login_required(views.dashboard), name="dashboard"),
    path('bussines-profile/',login_required(views.bussines), name="bussines"),
    path('perfil/<str:name>/<int:id>',login_required(views.profile), name="perfil"),
    path('edicion-perfil/<int:id>',login_required(views.editionProfile), name="edicionPerfil"),
    path('seleccionar-perfil',login_required(views.selectCatalog), name="selectPerfil"),
    path('agregar-catalogo/<int:id>',login_required(views.addCatalog), name="addCatalogo"),
    path('ver-catalogo/', login_required(views.viewCatalog), name="viewCatalogo"),
    path('edicion-catalogo/<int:id>', login_required(views.editCatalog), name="edicionCatalogo"),
    path('eliminar-catalogo/<int:id>', login_required(views.deleteCatalog), name="eliminarCatalogo"),
]



# cONFIGURACION PARA CARGAR IMAGENES
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path
from company import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path("registro", views.signUp, name="registro"),
    path("accounts/login/", views.logIn, name="ingreso"),
    path('logout/', views.logOut, name="logout"),
    path('creacion/', views.createAccount, name="creacion"),
    path('dashboard/',login_required(views.dashboard), name="dashboard"),
    path('bussines-profile/', views.bussines, name="bussines"),
]



# cONFIGURACION PARA CARGAR IMAGENES
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

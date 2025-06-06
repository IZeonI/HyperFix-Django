"""
URL configuration for hyperfix_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from productos import views as productos_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', lambda request: redirect('lista_componentes'), name='home'),

    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls'), name='productos'),
    
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('completar-datos/', productos_views.completar_datos_cliente, name='completar_datos_cliente'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', productos_views.registro, name='registro'),
]

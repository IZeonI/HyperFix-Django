from django.urls import path
from . import views

urlpatterns = [
    path('componentes/', views.lista_componentes, name='lista_componentes'),
]

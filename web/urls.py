from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),         # Página principal
    path('nivel/', views.nivel, name='nivel'), # Calculadora
]

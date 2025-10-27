from django.urls import path
from .views import home
from api.views import calcular  # tu API

urlpatterns = [
    path('', home, name='home'),              # la página principal
    path('api/calcular/', calcular, name='calcular'),  # tu API
]

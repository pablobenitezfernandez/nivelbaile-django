from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),       # Todo lo de la app web
    path('api/', include('api.urls')),   # Todo lo de la app API
]
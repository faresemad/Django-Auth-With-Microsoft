from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('', include('apps.authen.urls')),
]

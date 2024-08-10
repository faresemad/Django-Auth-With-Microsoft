from django.urls import path

from apps.authen import views

urlpatterns = [
    path('', views.index, name='index'),
]

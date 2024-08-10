from django.urls import path

from apps.authen import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login-no-sso/', views.login_no_sso, name='login_no_sso'),
    path('login-success/', views.login_success, name='login_success'),
]

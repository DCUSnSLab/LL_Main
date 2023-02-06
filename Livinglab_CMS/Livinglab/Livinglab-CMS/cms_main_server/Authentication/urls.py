from django.urls import path

from . import views

urlpatterns = [
    path('', views.Main, name='Main'),
    path('Login/', views.Login, name='Login'),
    path('Signup/', views.Signup, name='Signup'),
    path('Logout/', views.Logout, name='Logout'),

]
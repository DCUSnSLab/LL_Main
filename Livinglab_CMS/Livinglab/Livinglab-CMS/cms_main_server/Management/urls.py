from django.urls import path

from . import views

urlpatterns = [

    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('Dashboard_minor', views.Dashboard_minor, name='Dashboard_minor'),

    path('Admin/', views.Administration, name='Admin'),
    path('AdminChange/<int:id>', views.AdminChange, name='AdminChange'),
    path('ShowDetailAdmin/<int:id>', views.ShowDetailAdmin, name='ShowDetailAdmin'),
    path('Mypage/', views.Mypage, name='Mypage'),
    path('EditMyinfo/', views.EditMyinfo, name='EditMyinfo'),

    path('ViewShelter/', views.ViewShelter, name='ViewShelter'),
    path('RegisterShelter/', views.RegisterShelter, name='RegisterShelter'),
    path('ShowDetailShelter/<int:id>', views.ShowDetailShelter, name='ShowDetailShelter'),
    path('DeleteShelter/<int:id>', views.DeleteShelter, name='DeleteShelter'),
    path('UpdateShelterStatus/<int:id>', views.UpdateShelterStatus, name='UpdateShelterStatus'),

    path('ViewCommunity/', views.ViewCommunity, name='ViewCommunity'),
    path('RegisterCommunity', views.RegisterCommunity, name='RegisterCommunity'),
    path('ShowDetailCommunity/<int:id>', views.ShowDetailCommunity, name='ShowDetailCommunity'),
    path('UpdateCommunityStatus/<int:id>', views.UpdateCommunityStatus, name='UpdateCommunityStatus'),

    path('UpdateCommentStatus/<int:comuId>/<int:comenId>', views.UpdateCommentStatus, name='UpdateCommentStatus'),


    path('ViewAdvertisement/', views.ViewAdvertisement, name='ViewAdvertisement'),
    path('RegisterAdvertisement', views.RegisterAdvertisement, name='RegisterAdvertisement'),
    path('ShowDetailAdvertisement/<int:id>', views.ShowDetailAdvertisement, name='ShowDetailAdvertisement'),
    path('UpdateAdvertisementStatus/<int:id>', views.UpdateAdvertisementStatus, name='UpdateAdvertisementStatus'),

    path('ViewContent/', views.ViewContent, name='ViewContent'),
    path('UpdateContentStatus/<int:id>', views.UpdateContentStatus, name='UpdateContentStatus'),
    path('ShowDetailContent/<int:id>', views.ShowDetailContent, name='ShowDetailContent'),





]
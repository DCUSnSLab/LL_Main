from django.urls import path

from . import views

urlpatterns = [

    path('AddCommunityComment/<int:id>', views.AddCommunityComment, name='AddCommunityComment'),
    path('UploadContent/<int:id>', views.UploadContent, name='UploadContent')
    path('UploadAdvertisement/<int:id>', views.UploadAdvertisement, name='UploadAd'),
]
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('ShelterLogin.urls')),
    path('Service/', include('Service.urls')),
    path('admin/', admin.site.urls),
]

# 굉장히 중요, 경로지정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
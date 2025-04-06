from django.contrib import admin
from django.urls import path, include
from gallery import views # Import the views module from the gallery app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Gallery_Main, name='base'), # URL pattern for the gallery view
]

# for media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

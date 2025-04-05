from django.contrib import admin
from django.urls import path
from gallery import views # Import the views module from the gallery app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Gallery, name='gallery'), # URL pattern for the gallery view
]

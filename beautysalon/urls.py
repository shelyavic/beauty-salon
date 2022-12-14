"""beautysalon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#import os
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.static import serve

from beautysalon.settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': BASE_DIR / 'static/img',
        }
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
    path('users/', include('users.urls')),

    
]

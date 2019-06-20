"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from . import settings
from obp.admin import admin_site

admin.autodiscover()

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),

    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    path('obp/', include('obp.urls') ),

    path('admin/', admin.site.urls ),
    #path('obp/admin/', include('admin.site.urls') ),

    path('cart/', include('cart.urls') ),

    path('myadmin/', admin_site.urls ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

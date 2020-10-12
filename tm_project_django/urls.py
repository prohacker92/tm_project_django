"""tm_project_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import RedirectView
from my_app import views

urlpatterns = [
    path('', views.index,),
    re_path(r'^ajax/get_response/$', views.table, name='get_response'),
    path('home/', views.index,),
    path('accounts/', include('django.contrib.auth.urls')),
    path('view_sms/<int:id>/', views.view_sms),
    re_path(r'admin/', admin.site.urls),
    re_path(r'home/$', views.index),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('archive/', include('archive.urls')),
    path('ps/', include('signal_PS.urls')),
    path('contacts/', include('support_contacts.urls')),

]

"""EplanChecklistProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from checklists import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # AUTH
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),


    # Projects
    path('projects/', views.projects, name='projects'),
    # Single project
    path('projects/<int:project_pk>/', views.singleproject, name='singleproject'),
    # Single eplan
    path('projects/<int:project_pk>/<int:eplan_pk>',
         views.singleeplan, name='singleeplan'),
    # Eplan device
    path('projects/<int:project_pk>/<int:eplan_pk>/<int:eplandevice_pk>',
         views.eplandevice, name='eplandevice'),
    # Device checkpoint
    path('projects/<int:project_pk>/<int:eplan_pk>/<int:eplandevice_pk>/<int:checkpoint_pk>',
         views.checkpoint, name='checkpoint'),


    # Devices
    path('devices/', views.genericdevices, name='genericdevices'),
    # Single device
    path('devices/<int:device_pk>/', views.singledevice, name='singledevice'),

]
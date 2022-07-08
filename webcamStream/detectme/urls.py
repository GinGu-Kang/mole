from django.conf.urls import url, include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('detectme', views.detectme, name="detectme"),
    path('stop', views.stop, name="stop"),
    path('start', views.start, name="start"),
    
    ]
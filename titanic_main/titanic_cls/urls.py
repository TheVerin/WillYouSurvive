from django.urls import path
from . import views

urlpatterns = [
    path('', views.final, name='final'),
    path('died/', views.dead, name='dead'),
    path('alive/', views.alive, name='alive')]

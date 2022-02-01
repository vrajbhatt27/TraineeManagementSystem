from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('forms/<fid>/', views.tforms, name="tform"),
    path('toTdetails/<fid>/', views.toTdetails, name="toTdetails"),
    path('traineeDetails/', views.tdetails, name='tdetails')
]

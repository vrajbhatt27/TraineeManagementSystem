from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('forms/<fid>/', views.tforms, name="tform"),
    path('toTdetails/<fid>/', views.toTdetails, name="toTdetails"),
    path('traineeDetails/', views.tdetails, name='tdetails'),
    path('delTrainee/<temail>/', views.delTrainee, name='delTrainee'),
    path('setSession/<fid>/', views.setSession, name='setSession'),
    path('sendEmail/', views.sendEmail, name='sendEmail'),
    path('toogleUrlStatus/<fid>/', views.urlStatusToogle, name='urlStatusToogle'),
    path('gcsv/', views.download_csv, name='gcsv'),
    path('delForm/<fid>/', views.delForm, name='delForm'),
    path('generateCertificate/', views.generateCertificate,
         name='generateCertificate'),
    path('generateOfferLetter/', views.generateOfferLetter,
         name='generateOfferLetter'),

    # Test Module urls:
    path('createTest/', views.createTest, name='createTest'),
    path('tests/<tid>/', views.test_form, name="testForm"),
    path('filterTrainee/', views.filterTrainee, name="filterTrainee"),
    path('toogleTestStatus/<tid>/',
         views.toogleTestStatus, name="testStatusToogle"),
    path('delTest/<tid>/', views.delTest, name='delTest'),

    # Payment Module urls:
    path('payment/<fid>/', views.payment, name='payment'),
]

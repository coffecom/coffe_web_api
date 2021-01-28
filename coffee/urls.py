from django.contrib import admin
from django.urls import path, register_converter
from . import views
from datetime import datetime

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', views.getAllItems, name = 'all-items'),
    path('create-item', views.createItem, name = 'create-item'),
    path('get-item-by-id/<str:id>/', views.getItemById, name = 'get-item-by-id'),
    path('get-item-by-name/<str:name>/', views.getItemByName, name = 'get-item-by-name'),
    path('delete-item-by-id/<str:id>/', views.deleteItemById, name = 'delete-item-by-id'),
    path('delete-item-by-name/<str:name>/', views.deleteItemByName, name = 'delete-item-by-name'),
    path('patch-item-by-name/<str:name>/', views.patcItemByName, name = 'patch-item-by-name'),
    path('patch-item-by-id/<str:id>/', views.patcItemById, name = 'patch-item-by-id'),

    path('create-manager', views.createManager, name = 'create-manager'),
    path('create-barista', views.createBarista, name = 'create-barista'),

    path('create-day-shedule', views.createDayShechule, name = 'create-day-shedule'),
    path('get-day-shedule-date-by-id/<str:id>/', views.getDayShechuleById, name = 'get-day-shedule-date-by-id'),
    path('get-day-shedule-date-by-date/<yyyy:date>/', views.getDayShechuleByDate, name = 'get-day-shedule-date-by-date'),
    path('get-all-day-shedule', views.getAllDayShechules, name = 'get-all-day-shedule'),
    path('patch-day-shedule-by-id/<str:id>/', views.patchDayShechuleById, name = 'patch-day-shedule-by-id'),
    path('patch-day-shedule-by-date/<yyyy:date>/', views.patchDayShechuleByDate, name = 'patch-day-shedule-by-date'),

    path('auth', views.authentication, name = 'authentication')
]
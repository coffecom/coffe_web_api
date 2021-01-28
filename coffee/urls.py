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

    path('create-day-schedule', views.createDaySchedule, name = 'create-day-schedule'),
    path('get-day-schedule-date-by-id/<str:id>/', views.getDayScheduleById, name = 'get-day-schedule-date-by-id'),
    path('get-day-schedule-date-by-date/<yyyy:date>/', views.getDayScheduleByDate, name = 'get-day-schedule-date-by-date'),
    path('get-all-day-schedule', views.getAllDaySchedules, name = 'get-all-day-schedule'),
    path('patch-day-schedule-by-id/<str:id>/', views.patchDayScheduleById, name = 'patch-day-schedule-by-id'),
    path('patch-day-schedule-by-date/<yyyy:date>/', views.patchDayScheduleByDate, name = 'patch-day-schedule-by-date'),

    path('create-receipt', views.createReceipt, name = 'create-receipt'),
    path('get-receipt-by-id/<str:id>/', views.getReceiptById, name = 'get-receipt-by-id'),
    path('get-receipt-by-date/<yyyy:date>/', views.getReceiptByDate, name = 'get-receipt-by-date'),
    # path('patch-receipt/<str:id>/', views.patchReceiptById, name = 'patch-receipt'),
    path('delete-receipt/<str:id>/', views.deleteReceiptById, name = 'delete-receipt'),

    path('create-receipt-item', views.createReceiptItem, name = 'create-receipt-item'),
    path('delete-receipt-item/<str:id>/', views.deleteReceiptItem, name = 'delete-receipt-item'),
    path('patch-receipt-item/<str:id>/', views.patchReceiptItem, name = 'patch-receipt-item'),
    path('get-receipt-item/<str:id>/', views.getReceiptItem, name = 'get-receipt-item'),

    path('auth', views.authentication, name = 'authentication')
]
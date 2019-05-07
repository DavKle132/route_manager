from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('route_list/', views.route_list, name='route_list'),
    path('add_route/', views.add_route, name='add_route'),
    path('<slug:route_name>/', views.route, name='route'),
    path('<slug:route_name>/add_note/', views.add_note, name='add_note'),
    path('<slug:route_name>/checkout/', views.checkout, name='checkout'),
    path('<slug:route_name>/turnin/', views.turnin, name='turnin'),
]
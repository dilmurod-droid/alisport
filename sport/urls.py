from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('choice_tariff/', views.choice_tariff_view, name='choice_tariff'),
    path('admin_panel/', views.admin_panel_view, name='admin_panel'),
]

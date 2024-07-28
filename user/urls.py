from django.urls import path
from . import views
from .views import Create_user,user_list_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add_users/',Create_user.as_view(),name='add_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('users/send_sms/<int:user_id>/', views.send_sms_to_user_view, name='send_sms_to_user'),
    path('user_list',user_list_view,name='user_list')
]
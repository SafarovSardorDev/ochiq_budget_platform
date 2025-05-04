from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('project/<int:project_id>/', views.detail, name='detail'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin/', views.admin_page, name='admin_page'),
    path('tuman/', views.tuman, name='tuman'),
    path('user/', views.user_page, name='user'),
]
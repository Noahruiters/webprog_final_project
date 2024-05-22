from django.urls import path
from . import views

app_name = 'app_itmunch'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('questions/', views.questions_view, name='questions'),
]
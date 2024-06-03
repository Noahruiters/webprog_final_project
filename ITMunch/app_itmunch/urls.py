from django.urls import path
from . import views

app_name = 'app_itmunch'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('questions/', views.questions_view, name='questions'),
    path('edit/', views.questions_view, name='edit'),
    path('save_entry/', views.save_nutritionEntry, name='save_entry'), 
    path('load_entry/', views.load_nutritionEntries, name='load_entry'),#TODO: add variables I think
    path('delete_entry/', views.delete_nutritionEntry, name='delete_entry')#TODO: add variables I think
]
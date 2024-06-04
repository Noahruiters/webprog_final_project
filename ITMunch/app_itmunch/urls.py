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
    path('results/', views.search_results, name='search_results'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),

    #########################################################################
    ### THE CODE BELOW IS NOT USED BUT WAS KEPT TO SHOW WHAT WE WORKED ON ###
    #########################################################################

    path('save_entry/', views.save_nutritionEntry, name='save_entry'), 
    path('load_entry/', views.load_nutritionEntries, name='load_entry'),# todo: add variables I think
    path('delete_entry/', views.delete_nutritionEntry, name='delete_entry'),# todo: add variables I think
    path('add_to_cart/<int:fdcId>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
]
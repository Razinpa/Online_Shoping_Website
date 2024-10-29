from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    
     
    path('add_product/', views.add_product, name="add_product"),
    path('addandedit/', views.addandedit, name="addandedit"),
    path('edit_product/<int:product_id>/', views.edit_product, name="edit_product"),
    path('delete_product/<int:product_id>/', views.delete_product, name="delete_product"),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart/', views.cart, name="cart"),
]


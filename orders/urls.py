from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # PLACE ORDER
    path('place-order/', views.place_order, name='place_order'),

    # ORDER HISTORY
    path('order-history/', views.order_history, name='order_history'),

    # ORDER DETAILS
    path(
        'order-details/<int:order_id>/',
        views.order_details,
        name='order_details'
    ),

    # DELETE ORDER
    path(
        'delete-order/<int:order_id>/',
        views.delete_order,
        name='delete_order'
    ),

    # ADMIN DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # CUSTOMER REGISTRATION
    path('register/', views.register, name='register'),

    # CUSTOMER LOGIN
    path('login/', views.customer_login, name='login'),

    # CUSTOMER LOGOUT
    path('logout/', views.customer_logout, name='logout'),

    # CUSTOMER DASHBOARD
    path('my-account/', views.customer_dashboard, name='customer_dashboard'),

]
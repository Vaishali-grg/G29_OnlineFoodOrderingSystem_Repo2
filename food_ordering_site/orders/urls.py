# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
     path('register/', views.register_view, name='register'),
     path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
     path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('outlets/create/', views.create_outlet, name='create_outlet'),
    path('outlets/manage/', views.manage_outlets, name='manage_outlets'),
    path('outlets/<int:outlet_id>/menu/create/', views.create_menu, name='create_menu'),
    path('outlets/<int:outlet_id>/menu/manage/', views.manage_menus, name='manage_menus'),
     path('outlets/', views.outlet_list, name='outlet_list'),
     path('outlets/<int:outlet_id>/menus/', views.menu_list, name='menu_list'),
     path('add_to_cart/<int:menu_id>/', views.add_to_cart, name='add_to_cart'),
     path('cart/', views.view_cart, name='view_cart'),
     path('remove_from_cart/<int:menu_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('place_order/', views.place_order, name='place_order'),
     path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
     path('orders/', views.order_list, name='order_list'),
    #  path('order/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
     path('your_orders/', views.student_order_list, name='student_order_list'),  # Student view
    




    path('outlets/<int:outlet_id>/edit/', views.edit_outlet, name='edit_outlet'),
    path('outlets/<int:outlet_id>/delete/', views.delete_outlet, name='delete_outlet'),


    # urls.py

    path('outlet/<int:outlet_id>/menu/<int:menu_id>/edit/', views.edit_menu, name='edit_menu'),
    path('outlet/<int:outlet_id>/menu/<int:menu_id>/delete/', views.delete_menu, name='delete_menu'),



    path('favorite/outlet/<int:outlet_id>/', views.toggle_favorite_outlet, name='toggle_favorite_outlet'),
    path('favorite/menu/<int:menu_id>/', views.toggle_favorite_menu_item, name='toggle_favorite_menu_item'),




    path('favorites/', views.my_favorites, name='my_favorites'),
    path('favorites/menu/', views.my_favorite_menuitems, name='my_favorite_menuitems'),




    path('',views.home,name='home'),
    path('logout/', views.logout_view, name='logout'),


    path('profile/', views.profile_view, name='profile'),



    path('menu/<int:item_id>/rate/', views.rate_menu_item, name='rate_menu_item'),

    

]
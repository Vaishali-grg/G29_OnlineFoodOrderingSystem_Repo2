from django.urls import path
from . import views

urlpatterns = [
    path('types/', views.store_material_type_list, name='store_material_type_list'),
    path('types/add/', views.store_add_material_type, name='store_add_material_type'),
    path('types/edit/<int:pk>/', views.store_edit_material_type, name='store_edit_material_type'),
    path('types/delete/<int:pk>/', views.store_delete_material_type, name='store_delete_material_type'),

    path('materials/<int:type_id>/', views.store_material_list, name='store_material_list'),
    path('materials/add/<int:type_id>/', views.store_add_material, name='store_add_material'),
    path('materials/edit/<int:pk>/', views.store_edit_material, name='store_edit_material'),
    path('materials/delete/<int:pk>/', views.store_delete_material, name='store_delete_material'),

    # Student Interface
   path('student/types/', views.store_student_material_type_list, name='store_student_material_type_list'),
   path('student/materials/<int:type_id>/', views.store_student_material_list, name='store_student_material_list'),
   
# Cart/Checkout URLs
path('cart/', views.store_checkout_page, name='store_checkout_page'),
path('cart/add/<int:material_id>/', views.store_add_to_cart, name='store_add_to_cart'),

# Order Confirmation URL
path('order/confirmation/', views.store_order_confirmation, name='store_order_confirmation'),

]

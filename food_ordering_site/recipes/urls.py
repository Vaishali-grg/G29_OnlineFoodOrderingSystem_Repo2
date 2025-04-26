# recipes/urls.py

from django.urls import path
from . import views
from .views import create_recipe, recipe_list, recipe_detail, update_recipe, delete_recipe

urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('create/', create_recipe, name='create_recipe'),
    path('<int:pk>/', recipe_detail, name='recipe_detail'),
    path('<int:pk>/edit/', update_recipe, name='update_recipe'),
    path('<int:pk>/delete/', delete_recipe, name='delete_recipe'),
    path('categories/add/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.recipe_by_category, name='recipe_by_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),



    path('student/categories/', views.student_category_list, name='student_category_list'),
    path('student/category/<int:category_id>/recipes/', views.student_recipe_by_category, name='student_recipe_by_category'),
    path('student/recipe/<int:pk>/', views.student_recipe_detail, name='student_recipe_detail'),
]



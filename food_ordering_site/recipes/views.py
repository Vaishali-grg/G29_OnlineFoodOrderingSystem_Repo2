from django.shortcuts import render, redirect
from .forms import RecipeForm,CategoryForm
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# View to show all categories

@login_required
def category_list(request):
    if request.user.role == 'staff':
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})
    return HttpResponseForbidden("Access Denied: You are not a staff.")

# View to show recipes filtered by category

@login_required
def recipe_by_category(request, category_id):
    if request.user.role == 'staff':
        category = Category.objects.get(id=category_id)
        recipes = Recipe.objects.filter(category=category)
        return render(request, 'recipe_by_category.html', {'category': category, 'recipes': recipes})
    return HttpResponseForbidden("Access Denied: You are not a staff.")

@login_required
def create_recipe(request):
    if request.user.role == 'staff':
        if request.method == 'POST':
            form = RecipeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create_recipe')  # Redirect back to form or change to 'recipe_list'
        else:
            form = RecipeForm()
        return render(request, 'create_recipe.html', {'form': form})
    return HttpResponseForbidden("Access Denied: You are not a staff.")


@login_required
def recipe_list(request):
    if request.user.role == 'staff':
        recipes = Recipe.objects.all()
        return render(request, 'recipe_list.html', {'recipes': recipes})
    return HttpResponseForbidden("Access Denied: You are not a staff.")


@login_required
def recipe_list(request):
    if request.user.role == 'staff':
        category_id = request.GET.get('category')  # Get selected category from query string
        categories = Category.objects.all()

        if category_id:
            recipes = Recipe.objects.filter(category_id=category_id)
        else:
            recipes = Recipe.objects.all()

        context = {
            'recipes': recipes,
            'categories': categories,
            'selected_category': int(category_id) if category_id else None
        }
        return render(request, 'recipe_list.html', context)
    return HttpResponseForbidden("Access Denied: You are not a staff.")

@login_required
def recipe_detail(request, pk):
    if request.user.role == 'staff':
        recipe = get_object_or_404(Recipe, pk=pk)
        return render(request, 'recipe_detail.html', {'recipe': recipe})
    return HttpResponseForbidden("Access Denied: You are not a staff.")

# UPDATE VIEW
@login_required
def update_recipe(request, pk):
    if request.user.role == 'staff':
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            form = RecipeForm(request.POST, instance=recipe)
            if form.is_valid():
                form.save()
                return redirect('recipe_detail', pk=recipe.pk)
        else:
            form = RecipeForm(instance=recipe)
        return render(request, 'recipe_form.html', {'form': form, 'title': 'Update Recipe'})
    return HttpResponseForbidden("Access Denied: You are not a staff.")

# DELETE VIEW
@login_required
def delete_recipe(request, pk):
    if request.user.role == 'staff':
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            recipe.delete()
            return redirect('recipe_list')
        return render(request, 'confirm_delete.html', {'recipe': recipe})
    return HttpResponseForbidden("Access Denied: You are not a staff.")



# add Category
@login_required
def create_category(request):
    if request.user.role == 'staff':
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('category_list')
        else:
            form = CategoryForm()
        return render(request, 'category_form.html', {'form': form, 'title': 'Add Category'})
    return HttpResponseForbidden("Access Denied: You are not a staff.")

# edit Category
@login_required
def edit_category(request, category_id):
    if request.user.role == 'staff':
        category = get_object_or_404(Category, id=category_id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('category_list')  # replace with your actual category list view name
        else:
            form = CategoryForm(instance=category)
        return render(request, 'category_form.html', {'form': form, 'title': 'Edit Category'})
    return HttpResponseForbidden("Access Denied: You are not a staff.")


# delete Category
@login_required
def delete_category(request, category_id):
    if request.user.role == 'staff':
        category = get_object_or_404(Category, id=category_id)
        if request.method == 'POST':
            category.delete()
            return redirect('category_list')  # replace with your actual category list view name
        return render(request, 'confirm_delete1.html', {'object': category, 'type': 'Category'})
    return HttpResponseForbidden("Access Denied: You are not a staff.")






from django.shortcuts import render, get_object_or_404
from .models import Category, Recipe

@login_required
def student_category_list(request):
    if request.user.role == 'student':
        categories = Category.objects.all()
        return render(request, 'student/category_list.html', {'categories': categories})
    return HttpResponseForbidden("Access Denied: You are not a student.")



@login_required
def student_recipe_by_category(request, category_id):
    if request.user.role == 'student':
        category = get_object_or_404(Category, id=category_id)
        recipes = Recipe.objects.filter(category=category)
        return render(request, 'student/recipe_by_category.html', {
            'category': category,
            'recipes': recipes
        })
    return HttpResponseForbidden("Access Denied: You are not a student.")

@login_required
def student_recipe_detail(request, pk):
    if request.user.role == 'student':
        recipe = get_object_or_404(Recipe, pk=pk)
        return render(request, 'student/recipe_detail.html', {
            'recipe': recipe
        })
    return HttpResponseForbidden("Access Denied: You are not a student.")

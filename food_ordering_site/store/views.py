from django.shortcuts import render, redirect, get_object_or_404
from .models import StoreMaterialType, StoreMaterial
from .forms import StoreMaterialTypeForm, StoreMaterialForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Material Type Views
@login_required
def store_material_type_list(request):
    if request.user.role == 'manager':
        types = StoreMaterialType.objects.all()
        return render(request, 'store/material_type_list.html', {'types': types})
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def store_add_material_type(request):
    if request.user.role == 'manager':
        if request.method == 'POST':
            form = StoreMaterialTypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('store_material_type_list')
        else:
            form = StoreMaterialTypeForm()
        return render(request, 'store/material_type_form.html', {'form': form})
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def store_edit_material_type(request, pk):
    if request.user.role == 'manager':
        material_type = get_object_or_404(StoreMaterialType, pk=pk)
        if request.method == 'POST':
            form = StoreMaterialTypeForm(request.POST, instance=material_type)
            if form.is_valid():
                form.save()
                return redirect('store_material_type_list')
        else:
            form = StoreMaterialTypeForm(instance=material_type)
        return render(request, 'store/material_type_form.html', {'form': form})
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def store_delete_material_type(request, pk):
    if request.user.role == 'manager':
        material_type = get_object_or_404(StoreMaterialType, pk=pk)
        material_type.delete()
        return redirect('store_material_type_list')
    return HttpResponseForbidden("Access Denied: You are not a manager.")

# Material Views
@login_required
def store_material_list(request, type_id):
    if request.user.role == 'manager':
        material_type = get_object_or_404(StoreMaterialType, id=type_id)
        materials = StoreMaterial.objects.filter(material_type=material_type)
        return render(request, 'store/material_list.html', {'materials': materials, 'material_type': material_type})
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def store_add_material(request, type_id):
    if request.user.role == 'manager':
        material_type = get_object_or_404(StoreMaterialType, id=type_id)
        if request.method == 'POST':
            form = StoreMaterialForm(request.POST)
            if form.is_valid():
                material = form.save(commit=False)
                material.material_type = material_type
                material.save()
                return redirect('store_material_list', type_id=type_id)
        else:
            form = StoreMaterialForm()
        return render(request, 'store/material_form.html', {'form': form, 'material_type': material_type})
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def store_edit_material(request, pk):
    if request.user.role == 'manager':
        material = get_object_or_404(StoreMaterial, pk=pk)
        if request.method == 'POST':
            form = StoreMaterialForm(request.POST, instance=material)
            if form.is_valid():
                form.save()
                return redirect('store_material_list', type_id=material.material_type.id)
        else:
            form = StoreMaterialForm(instance=material)
        return render(request, 'store/material_form.html', {'form': form, 'material_type': material.material_type})
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def store_delete_material(request, pk):
    if request.user.role == 'manager':
        material = get_object_or_404(StoreMaterial, pk=pk)
        type_id = material.material_type.id
        material.delete()
        return redirect('store_material_list', type_id=type_id)
    return HttpResponseForbidden("Access Denied: You are not a manager.")



# Student Interface Views

@login_required
def store_student_material_type_list(request):
    if request.user.role == 'student':
        types = StoreMaterialType.objects.all()
        return render(request, 'store/student_material_type_list.html', {'types': types})
    return HttpResponseForbidden("Access Denied: You are not a student.")

@login_required
def store_student_material_list(request, type_id):
    if request.user.role == 'student':
        material_type = get_object_or_404(StoreMaterialType, id=type_id)
        materials = StoreMaterial.objects.filter(material_type=material_type)
        return render(request, 'store/student_material_list.html', {
            'material_type': material_type,
            'materials': materials
        })
    return HttpResponseForbidden("Access Denied: You are not a student.")


from django.shortcuts import redirect

@login_required
def store_add_to_cart(request, material_id):
    if request.user.role == 'student':
        material = get_object_or_404(StoreMaterial, id=material_id)
        cart = request.session.get('cart', {})

        quantity = int(request.POST.get('quantity', 1))

        if str(material_id) in cart:
            cart[str(material_id)]['quantity'] += quantity
        else:
            cart[str(material_id)] = {
                'name': material.name,
                'price': float(material.price),
                'quantity': quantity,
                'image_url': material.image_url
            }

        request.session['cart'] = cart
        return redirect('store_checkout_page')  # Redirect to cart page after adding product
    return HttpResponseForbidden("Access Denied: You are not a student.")

@login_required
def store_checkout_page(request):
    if request.user.role == 'student':
        cart = request.session.get('cart', {})

        if request.method == 'POST':
            # Handle update quantity or remove items from cart
            material_id = request.POST.get('material_id')
            action = request.POST.get('action')
            
            if action == 'update':
                quantity = int(request.POST.get('quantity'))
                if str(material_id) in cart:
                    cart[str(material_id)]['quantity'] = quantity
            elif action == 'remove':
                if str(material_id) in cart:
                    del cart[str(material_id)]

            request.session['cart'] = cart

        return render(request, 'store/store_checkout.html', {'cart': cart})
    return HttpResponseForbidden("Access Denied: You are not a student.")

@login_required
def store_edit_cart(request, material_id):
    if request.user.role == 'student':
        if request.method == 'POST':
            cart = request.session.get('cart', {})
            quantity = int(request.POST.get('quantity', 1))
            if str(material_id) in cart:
                cart[str(material_id)]['quantity'] = quantity
                request.session['cart'] = cart
        return redirect('store_checkout_page')  # Corrected to point to checkout page
    return HttpResponseForbidden("Access Denied: You are not a student.")


@login_required
def store_remove_from_cart(request, material_id):
    if request.user.role == 'student':
        cart = request.session.get('cart', {})
        if str(material_id) in cart:
            del cart[str(material_id)]
            request.session['cart'] = cart
        return redirect('store_checkout_page')  # Corrected to point to checkout page
    return HttpResponseForbidden("Access Denied: You are not a student.")


@login_required
def store_order_confirmation(request):
    if request.user.role == 'student':
        cart = request.session.get('cart', {})
        total_amount = sum(item['price'] * item['quantity'] for item in cart.values())  # Calculate total price

        # Optionally, clear the cart after order confirmation
        if cart:
            request.session['cart'] = {}

        return render(request, 'store/store_order_confirmation.html', {
            'cart': cart,
            'total_amount': total_amount
        })
    return HttpResponseForbidden("Access Denied: You are not a student.")


from django.shortcuts import render

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def staff_dashboard(request):
    if request.user.role == 'staff':
        return render(request, 'staff_dashboard.html')
    return HttpResponseForbidden("Not allowed")







# yourapp/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Redirect based on role
            if user.role == 'manager': 
                return redirect('manager_dashboard')
            elif user.role == 'staff':
                return redirect('staff_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# yourapp/views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            login(request, user)
            return redirect('login')  # or role-based redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# yourapp/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

@login_required
def manager_dashboard(request):
    if request.user.role == 'manager':
        return render(request, 'manager_dashboard.html')
    return HttpResponseForbidden("Access Denied: You are not a manager.")

@login_required
def staff_dashboard(request):
    if request.user.role == 'staff':
        return render(request, 'staff_dashboard.html')
    return HttpResponseForbidden("Access Denied: You are not a staff.")

@login_required
def student_dashboard(request):
    if request.user.role == 'student':
        return render(request, 'student_dashboard.html')
    return HttpResponseForbidden("Access Denied: You are not a student.")
















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Outlet, Menu
from .forms import OutletForm, MenuForm
# from .decorators import manager_required  # Import the decorator

@login_required
def create_outlet(request):
    if request.user.role == 'manager':
        if request.method == 'POST':
            form = OutletForm(request.POST)
            if form.is_valid():
                outlet = form.save(commit=False)
                outlet.manager = request.user  # Set the logged-in user as the manager
                outlet.save()
                return redirect('manage_outlets')  # Redirect to a page that lists outlets
        else:
            form = OutletForm()
        return render(request, 'users/create_outlet.html', {'form': form})
    return HttpResponseForbidden("Access Denied: You are not a manager.")


@login_required
def manage_outlets(request):
    if request.user.role == 'manager':

        outlets = Outlet.objects.filter(manager=request.user)
        return render(request, 'users/manage_outlets.html', {'outlets': outlets})
    return HttpResponseForbidden("Access Denied: You are not a manager.")


@login_required
def create_menu(request, outlet_id):
    if request.user.role == 'manager':
        outlet = get_object_or_404(Outlet, id=outlet_id, manager=request.user)
        if request.method == 'POST':
            form = MenuForm(request.POST)
            if form.is_valid():
                menu = form.save(commit=False)
                menu.outlet = outlet
                menu.save()
                return redirect('manage_menus', outlet_id=outlet.id)
        else:
            form = MenuForm()
        return render(request, 'users/create_menu.html', {'form': form, 'outlet': outlet})
    return HttpResponseForbidden("Access Denied: You are not a manager.")


@login_required
def manage_menus(request, outlet_id):
    if request.user.role == 'manager':
        outlet = get_object_or_404(Outlet, id=outlet_id, manager=request.user)
        # menus = outlet.menus.all()
        menus = outlet.menus.all().prefetch_related('ratings')
        return render(request, 'users/manage_menus.html', {'outlet': outlet, 'menus': menus})
    return HttpResponseForbidden("Access Denied: You are not a manager.")






from django.shortcuts import render
from .models import Outlet, Menu

@login_required
def outlet_list(request):
    if request.user.role == 'student':
        favorite_outlet_ids = FavoriteOutlet.objects.filter(user=request.user).values_list('outlet_id', flat=True)
        outlets = Outlet.objects.all()
        return render(request, 'outlet_list.html', {'outlets': outlets,'favorite_outlet_ids': favorite_outlet_ids,})
    return HttpResponseForbidden("Access Denied: You are not a student.")


@login_required
def menu_list(request, outlet_id):
    if request.user.role == 'student':
        favorite_menu_ids = FavoriteMenuItem.objects.filter(user=request.user).values_list('menu_item_id', flat=True)
        outlet = Outlet.objects.get(id=outlet_id)
        menus = outlet.menus.all()
        return render(request, 'menu_list.html', {'outlet': outlet, 'menus': menus,'favorite_menu_ids': favorite_menu_ids,})
    return HttpResponseForbidden("Access Denied: You are not a student.")


from django.shortcuts import redirect, get_object_or_404
from .models import Menu ,Cart  # Import the Cart class

@login_required
def add_to_cart(request, menu_id):
    if request.user.role == 'student':
        menu_item = get_object_or_404(Menu, id=menu_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart = Cart(request)
        cart.add(menu_item, quantity)
        
        return redirect('menu_list', outlet_id=menu_item.outlet.id)
    return HttpResponseForbidden("Access Denied: You are not a student.")
# views.py

@login_required
def view_cart(request):
    if request.user.role == 'student':
        cart = Cart(request)
        return render(request, 'cart.html', {'cart': cart})
    return HttpResponseForbidden("Access Denied: You are not a student.")

# views.py

@login_required
def remove_from_cart(request, menu_id):
    if request.user.role == 'student':
        menu_item = get_object_or_404(Menu, id=menu_id)
        cart = Cart(request)
        cart.remove(menu_item)
        return redirect('view_cart')
    return HttpResponseForbidden("Access Denied: You are not a student.")



# views.py

from django.shortcuts import render, redirect
from .models import Order, OrderItem,Cart

@login_required
def place_order(request):
    if request.user.role == 'student':
        cart = Cart(request)
        if request.method == 'POST':
            # Create an order
            order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
            
            # Create order items
            for menu_id, item in cart.cart.items():
                menu_item = get_object_or_404(Menu, id=menu_id)
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item['quantity'])
            
            # Clear the cart
            cart.clear()
            
            return redirect('order_confirmation', order_id=order.id)
        
        return render(request, 'place_order.html', {'cart': cart})
    return HttpResponseForbidden("Access Denied: You are not a student.")


# views.py
@login_required
def order_confirmation(request, order_id):
    if request.user.role == 'student':
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'order_confirmation.html', {'order': order})
    return HttpResponseForbidden("Access Denied: You are not a student.")





@login_required
def order_list(request):
    if request.user.role != 'staff':
        return HttpResponseForbidden("Access Denied: You are not a staff.")
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        try:
            order = Order.objects.get(id=order_id)
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
        except Order.DoesNotExist:
            pass  # Handle error if needed

        return redirect('order_list')  # Refresh the same page

    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})






# views.py

from django.shortcuts import render
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def student_order_list(request):
    if request.user.role == 'student':
        orders = Order.objects.filter(user=request.user)  # Retrieve orders for the logged-in user
        return render(request, 'student_order_list.html', {'orders': orders})
    return HttpResponseForbidden("Access Denied: You are not a student.")













@login_required
def edit_outlet(request, outlet_id):
    if request.user.role == 'manager':
        outlet = get_object_or_404(Outlet, id=outlet_id, manager=request.user)
        if request.method == 'POST':
            form = OutletForm(request.POST, instance=outlet)
            if form.is_valid():
                form.save()
                return redirect('manage_outlets')
        else:
            form = OutletForm(instance=outlet)
        return render(request, 'users/edit_outlet.html', {'form': form, 'outlet': outlet})
    return HttpResponseForbidden("Access Denied: You are not a manager.")


@login_required
def delete_outlet(request, outlet_id):
    if request.user.role == 'manager':
        outlet = get_object_or_404(Outlet, id=outlet_id, manager=request.user)
        if request.method == 'POST':
            outlet.delete()
            return redirect('manage_outlets')
        return render(request, 'users/confirm_delete_outlet.html', {'outlet': outlet})
    return HttpResponseForbidden("Access Denied: You are not a manager.")





# views.py

@login_required
def edit_menu(request, outlet_id, menu_id):
    if request.user.role == 'manager':
        menu = get_object_or_404(Menu, id=menu_id, outlet__id=outlet_id, outlet__manager=request.user)
        if request.method == 'POST':
            form = MenuForm(request.POST, instance=menu)
            if form.is_valid():
                form.save()
                return redirect('manage_menus', outlet_id=outlet_id)
        else:
            form = MenuForm(instance=menu)
        return render(request, 'users/edit_menu.html', {'form': form, 'menu': menu, 'outlet_id': outlet_id})
    return HttpResponseForbidden("Access Denied")

@login_required
def delete_menu(request, outlet_id, menu_id):
    if request.user.role == 'manager':
        menu = get_object_or_404(Menu, id=menu_id, outlet__id=outlet_id, outlet__manager=request.user)
        if request.method == 'POST':
            menu.delete()
            return redirect('manage_menus', outlet_id=outlet_id)
        return render(request, 'users/confirm_delete_menu.html', {'menu': menu, 'outlet_id': outlet_id})
    return HttpResponseForbidden("Access Denied")

# views.py

from django.shortcuts import redirect, get_object_or_404
from .models import FavoriteOutlet, FavoriteMenuItem, Outlet, Menu

@login_required
def toggle_favorite_outlet(request, outlet_id):
    if request.method == 'POST':
        outlet = get_object_or_404(Outlet, id=outlet_id)
        fav, created = FavoriteOutlet.objects.get_or_create(user=request.user, outlet=outlet)
        if not created:
            fav.delete()
        return redirect(request.POST.get('next', 'outlet_list'))  # redirect back

@login_required
def toggle_favorite_menu_item(request, menu_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(Menu, id=menu_id)
        fav, created = FavoriteMenuItem.objects.get_or_create(user=request.user, menu_item=menu_item)
        if not created:
            fav.delete()
        return redirect(request.POST.get('next', 'menu_list'))  # redirect back
    






from .models import Outlet, FavoriteOutlet

@login_required
def my_favorites(request):
    favorite_outlets = Outlet.objects.filter(
        id__in=FavoriteOutlet.objects.filter(user=request.user).values_list('outlet_id', flat=True)
    )
    return render(request, 'my_favorites.html', {
        'favorite_outlets': favorite_outlets
    })


from django.contrib.auth.decorators import login_required
from .models import Menu, FavoriteMenuItem

@login_required
def my_favorite_menuitems(request):
    favorite_ids = FavoriteMenuItem.objects.filter(user=request.user).values_list('menu_item_id', flat=True)
    favorite_items = Menu.objects.filter(id__in=favorite_ids)
    return render(request, 'my_favorite_menuitems.html', {
        'favorite_items': favorite_items
    })








from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout




@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, MenuItemRating
from .forms import MenuItemRatingForm
from django.contrib.auth.decorators import login_required

@login_required
def rate_menu_item(request, item_id):
    menu_item = get_object_or_404(Menu, id=item_id)

    try:
        rating_instance = MenuItemRating.objects.get(user=request.user, menu_item=menu_item)
    except MenuItemRating.DoesNotExist:
        rating_instance = None

    if request.method == 'POST':
        form = MenuItemRatingForm(request.POST, instance=rating_instance)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.menu_item = menu_item
            rating.save()
            return redirect('menu_list', outlet_id=menu_item.outlet.id)
    else:
        form = MenuItemRatingForm(instance=rating_instance)

    return render(request, 'rate_menu_item.html', {
        'form': form,
        'menu_item': menu_item
    })
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)










from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Outlet(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255,default='no location provided')  # You can also use a more complex structure if needed
    image_url = models.URLField(max_length=10000, blank=True, null=True,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROdV0NHChvD7euSYRG-Y6bgwmFVPn_5A2suA&s')  # URL for the outlet image
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Menu(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,)
    image_url = models.URLField(max_length=10000, blank=True, null=True,default='https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQKfg7N2USWzRLIVY11-cCspadChLECuuhy7RBhe-_CfVv8Fw0o9bgJmNQozQLLLubb1vYlUQ')  # URL for the menu item image
    preparation_time = models.PositiveIntegerField(default=10)  # estimated time in minutes


    def __str__(self):
        return self.name
    
    # def average_rating(self):
    #     ratings = self.ratings.all()
    #     if ratings.exists():
    #         return round(sum(r.rating for r in ratings) / ratings.count(), 1)
    #     return None

    def average_rating(self):
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg or 0, 1)




class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Save an empty cart in the session
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1):
        """Add a menu item to the cart."""
        menu_id = str(menu_item.id)
        if menu_id not in self.cart:
            self.cart[menu_id] = {'quantity': 0, 'price': str(menu_item.price)}
        self.cart[menu_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Save the cart to the session."""
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, menu_item):
        """Remove a menu item from the cart."""
        menu_id = str(menu_item.id)
        if menu_id in self.cart:
            del self.cart[menu_id]
            self.save()

    def get_total_price(self):
        """Calculate the total price of the cart."""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Clear the cart."""
        del self.session['cart']
        self.session.modified = True





# models.py

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
       ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('picked', 'Picked'),
        ('prepared', 'Prepared'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} on {self.created_at}"
    
# models.py

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Order {self.order.id}"
    





# models.py

class FavoriteOutlet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'outlet')

class FavoriteMenuItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'menu_item')



class MenuItemRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'menu_item')  # Each user can rate a menu item only once

    def __str__(self):
        return f"{self.user.username} rated {self.menu_item.name} {self.rating}/5"
    
    
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

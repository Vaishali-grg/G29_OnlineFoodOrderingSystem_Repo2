from django.db import models

class StoreMaterialType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)  # Add image URL field

    def __str__(self):
        return self.name

class StoreMaterial(models.Model):
    material_type = models.ForeignKey(StoreMaterialType, on_delete=models.CASCADE, related_name='store_materials')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)  # Add image URL field

    def __str__(self):
        return self.name

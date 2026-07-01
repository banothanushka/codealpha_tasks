from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)       # Product Peru
    description = models.TextField()               # Product details
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    image = models.ImageField(upload_to='products/',blank=True, null=True)
    def _str__(self):
                return self.name


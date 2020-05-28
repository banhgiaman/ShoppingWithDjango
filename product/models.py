from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=45, default='')
    slug = models.CharField(max_length=45, default='')
    description = models.CharField(max_length=45, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=1024, default='')
    active = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(null=True, default=None, blank=True)
    is_new = models.BooleanField(default=False)
    img = models.ImageField(upload_to='static/homepage/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    actual_price = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    img = models.ImageField(upload_to='static/homepage/images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=45, default='')
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField(max_length=1024, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_buyer = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title

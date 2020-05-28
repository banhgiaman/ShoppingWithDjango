from django.contrib import admin
from .models import Product, Category, Image, Comment
# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'discount', 'is_new', 'active', 'price', 'category')
    list_editable = ('description', 'active', 'price', 'category')


class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description', 'active')


class AdminImage(admin.ModelAdmin):
    list_display = ('id', 'img', 'product')
    list_editable = ('product',)


class AdminComment(admin.ModelAdmin):
    list_display = ('id', 'comment', 'product')
    list_editable = ('product',)


admin.site.register(Comment, AdminComment)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Image, AdminImage)
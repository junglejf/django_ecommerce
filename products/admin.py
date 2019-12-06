from django.contrib import admin

# Register your models here.
from .models import Product, Category # equivalente a from product.models import Product

class ProductAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'slug')
	class meta:
		model = Product

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'slug')
	class meta:
		model = Category

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
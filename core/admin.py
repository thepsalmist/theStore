from django.contrib import admin
from .models import Item, Order, OrderItem, Category, Brands

# admin.site.register(Item)
# admin.site.register(OrderItem)
# admin.site.register(Order)
# admin.site.register(Category)
# admin.site.register(Brands)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "price", "category", "brand", "timestamp", "label"]
    list_filter = ["category", "brand"]
    list_editable = ["price", "category", "brand"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ["item", "ordered", "quantity"]


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ["user", "ordered", "startdate", "ordered_date"]


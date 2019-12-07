from django.contrib import admin
from .models import Item, Order, OrderItem, Category, Brand


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "price", "category", "brand", "timestamp", "label"]
    list_filter = ["category", "brand"]
    list_editable = ["price", "category", "brand"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["item", "ordered", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "ordered", "startdate", "ordered_date"]


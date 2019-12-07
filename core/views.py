from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from .models import Item, Order, OrderItem, Category, Brand


def item_list(request):
    items = Item.objects.filter(available=True)
    categories = Category.objects.all
    brands = Brand.objects.all
    context = {"items": items,"categories": categories, "brands": brands}
    return render(request, "core/shop.html", context)


def index(request, category_slug=None):
    category = None
    items = Item.objects.filter(available=True)[:6]
    categories = Category.objects.all
    brands = Brand.objects.all
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        items = items.filter(category=category)
    context = {"items": items,"category":category, "categories": categories, "brands": brands}
    return render(request, "core/index.html", context)


def product_detail(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    context = {"item": item}
    return render(request, "core/product.html", context)


# class ProductDetailView(DetailView):
#     model = Item
#     template_name = "core/product.html"
#     context_object_name = "items"


def add_to_cart(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    # filter the order by user, ordered =false we're getting non-completed orders
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
    else:
        messages.info(request, "This item quantity was updated")
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect("core:product", id=id, slug=slug)


def remove_from_cart(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            message.info(request, "This item was removed from your cart")
        else:
            message.info(request, "This item was removed from your cart")
            redirect("core:product", id=id, slug=slug)
    else:
        message.info(request, "You do not have an active order")
        return redirect("core:product", id=id, slug=slug)


def contact(request):
    return render(request, "core/contact-us.html", {})


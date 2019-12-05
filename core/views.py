from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone

from .models import Item, Order, OrderItem, Category, Brands


def item_list(request):
    items = Item.objects.all
    categories = Category.objects.all
    brands = Brands.objects.all
    context = {"items": items, "categories": categories, "brands": brands}
    return render(request, "core/shop.html", context)


def index(request):
    items = Item.objects.order_by("-timestamp")[:6]
    categories = Category.objects.all
    brands = Brands.objects.all
    context = {"items": items, "categories": categories, "brands": brands}
    return render(request, "core/index.html", context)


class ProductDetailView(DetailView):
    model = Item
    template_name = "core/product.html"
    context_object_name = "items"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.create(
        item=item, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order_item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    return redirect("core:product", slug=slug)


def contact(request):
    return render(request, "core/contact-us.html", {})


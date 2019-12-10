from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from .models import Item, Order, OrderItem, Category, Brand


def item_list(request):
    queryset = Item.objects.filter(available=True)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    paginator = Paginator(queryset, 6)
    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "page": page,
        "categories": categories,
        "brands": brands,
    }
    return render(request, "core/shop.html", context)


def index(request, category_slug=None):
    category = None
    items = Item.objects.filter(available=True)[:6]
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
    context = {
        "items": items,
        "category": category,
        "categories": categories,
        "brands": brands,
    }
    return render(request, "core/index.html", context)


def product_detail(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {"item": item, "categories": categories, "brands": brands}
    return render(request, "core/product.html", context)


@login_required
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
            return redirect("core:cart")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("core:cart")
    else:
        messages.info(request, "This item quantity was updated")
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect("core:cart")


@login_required
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
            messages.info(request, "This item was removed from your cart")
            return redirect("core:product", id=id, slug=slug)
        else:
            messages.info(request, "This item was removed from your cart")
            return redirect("core:product", id=id, slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", id=id, slug=slug)


@login_required
def remove_item_from_cart(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item was quantity was updated")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was removed from your cart")
            return redirect("core:product", id=id, slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", id=id, slug=slug)


def contact(request):
    return render(request, "core/contact-us.html", {})


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            return render(self.request, "core/cart.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


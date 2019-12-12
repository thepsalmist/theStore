from django.urls import path

from . import views
from .views import (
    item_list,
    index,
    product_detail,
    add_to_cart,
    remove_from_cart,
    remove_item_from_cart,
    contact,
    OrderSummaryView,
    CheckOutView,
)

app_name = "core"

urlpatterns = [
    path("", views.index, name="home"),
    path("shop/", views.item_list, name="shop"),
    path("product/<slug:slug>/<int:id>/", views.product_detail, name="product"),
    path("add_to_cart/<slug:slug>/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart/<slug:slug>/<int:id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "remove_item_from_cart/<slug:slug>/<int:id>/",
        views.remove_item_from_cart,
        name="remove_item_from_cart",
    ),
    path("cart/", OrderSummaryView.as_view(), name="cart"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("contact/", views.contact, name="contact"),
]


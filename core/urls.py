from django.urls import path

from . import views
from .views import item_list, index, product_detail, add_to_cart, contact

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
    path("contact/", views.contact, name="contact"),
]


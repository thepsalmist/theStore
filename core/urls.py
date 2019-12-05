from django.urls import path
from . import views
from .views import item_list, index, ProductDetailView, add_to_cart, contact

app_name = "core"

urlpatterns = [
    path("", views.index, name="home"),
    path("shop/", views.item_list, name="shop"),
    path("product/<slug>/", ProductDetailView.as_view(), name="product"),
    path("add_to_cart/<slug>/", views.add_to_cart, name="add_to_cart"),
    path("contact/", views.contact, name="contact"),
]

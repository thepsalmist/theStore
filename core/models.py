from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from PIL import Image


# create label choices
LABEL_CHOICES = (("P", "primary"), ("S", "secondary"), ("D", "danger"))


class Category(models.Model):
    # create tuple, first category goes to dB second displayed on screen
    CATEGOTY_CHOICES = (
        ("ED", "Education"),
        ("BS", "Business"),
        ("DS", "Design"),
        ("SC", "Security"),
        ("GM", "Games"),
    )
    title = models.CharField(choices=CATEGOTY_CHOICES, max_length=2, default="BS")

    def __str__(self):
        return self.title


class Brands(models.Model):
    BRAND_CHOICES = (
        ("MS", "Microsoft"),
        ("AD", "Adobe"),
        ("AV", "Avast"),
        ("KS", "Kaspersky"),
        ("NT", "Norton"),
    )
    title = models.CharField(choices=BRAND_CHOICES, max_length=2, default="MS")

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    brand = models.OneToOneField(
        Brands, on_delete=models.CASCADE, blank=True, null=True
    )
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default="P")
    image = models.ImageField(default="default.jpg", upload_to="items")
    slug = models.SlugField(default="test-product")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    startdate = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

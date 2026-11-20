from django.db import models
from django.conf import settings


class Order(models.Model):

    PAYMENT_CHOICES = [
        ("Cash on Delivery", "Cash on Delivery"),
        ("UPI", "UPI"),
        ("Card Payment", "Card Payment"),
    ]

    # Connect order to a registered customer account
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pizza_orders"
    )

    customer_name = models.CharField(max_length=100)

    order_id = models.CharField(
        max_length=20,
        unique=True
    )

    # Prevent duplicate order submissions
    submission_token = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True
    )

    # Pizza billing information
    bill_items = models.JSONField(default=list)

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    final_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Payment information
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES,
        default="Cash on Delivery"
    )

    # Order date and time
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer_name} - {self.order_id}"
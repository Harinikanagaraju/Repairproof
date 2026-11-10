from django.db import models
from django.contrib.auth.models import User
from datetime import date
import calendar


def add_months(original_date, months):
    month_index = original_date.month - 1 + months
    year = original_date.year + month_index // 12
    month = month_index % 12 + 1

    day = min(
        original_date.day,
        calendar.monthrange(year, month)[1]
    )

    return date(year, month, day)


class Appliance(models.Model):

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Kitchen', 'Kitchen'),
        ('Home Appliances', 'Home Appliances'),
        ('Other', 'Other'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    purchase_date = models.DateField()
    warranty_months = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bill = models.FileField(
        upload_to='bills/',
        blank=True,
        null=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def warranty_end(self):
        return add_months(
            self.purchase_date,
            self.warranty_months
        )

    @property
    def warranty_status(self):
        remaining = (self.warranty_end - date.today()).days

        if remaining < 0:
            return "Expired"
        elif remaining <= 30:
            return "Expiring Soon"
        return "Active"

    def __str__(self):
        return self.name
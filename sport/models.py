from datetime import timedelta, timezone
import datetime
from django.db import models

from user.models import BotUser

TARIFF_TYPE_STATUS = (
    ('daily', 'Daily'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly')
)
TARIFF_TYPE = (
    ('everyday', 'Every-Day'),
    ('in_one_day', 'In-one-day'),
)

class Tariff(models.Model):
    name = models.CharField(max_length=100)
    tariff_type = models.CharField(max_length=10, choices=TARIFF_TYPE_STATUS, default='daily')
    every_or_one = models.CharField(max_length=10, choices=TARIFF_TYPE, default='in_one_day')
    price = models.IntegerField()
    days = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Tariff"


class Payment(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    success = models.BooleanField(default=False)
    check_image_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Payment"

    def __str__(self):
        return f"{self.user}"


class OrderedTariffs(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    days = models.IntegerField(default=1)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "OrderedTariffs"

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = datetime.datetime.now().date()
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.days)
        super(OrderedTariffs, self).save(*args, **kwargs)

    def calculate_duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None
    def __str__(self):
        return f"{self.user}:{self.tariff}"

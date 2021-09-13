import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.shortcuts import redirect


class PhoneModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    phone = models.CharField(max_length=140)

    def __str__(self):
        return self.phone

    def get_absolute_url(self):
        return reverse('phone_model', args=[self.id])


class Fault(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    fault = models.CharField(max_length=140)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.fault

    def get_absolute_url(self):
        return reverse('faults', args=[self.id])


class BookingType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    booking_type = models.CharField(max_length=140)

    def __str__(self):
        return self.booking_type

    def get_absolute_url(self):
        return reverse('booking_type', args=[self.id])






class Booking(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    email = models.EmailField()
    phone = models.ForeignKey(PhoneModel, on_delete=models.CASCADE)
    fault = models.ForeignKey(Fault, on_delete=models.CASCADE)
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    booking_date = models.DateField()
    approve_booking = models.BooleanField(default=False)
    count_bookings = models.IntegerField(default=1, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)
    arrived = models.BooleanField(default=False)
    repaired = models.BooleanField(default=False)
    collected = models.BooleanField(default=False)
    refuse = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created', 'booking_date']

    def get_absolute_url(self):
        return redirect('all_bookings')


from django.contrib import admin
from .models import PhoneModel, Fault, BookingType, Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['email', 'author', 'phone', 'fault', 'booking_type', 'created', 'booking_date',
                    'approve_booking', 'count_bookings', 'comment', 'arrived', 'repaired', 'collected', 'refuse']
    list_filter = ['phone', 'fault', 'booking_type', 'booking_date', 'approve_booking', 'count_bookings']
    list_editable = ['approve_booking', 'count_bookings', 'arrived', 'repaired', 'collected', 'refuse']
    can_delete = False


# Register your models here.
admin.site.register(PhoneModel)
admin.site.register(Fault)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingType)

from django import forms
from django.forms import ModelForm
from .models import Booking
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        widgets = {
            'booking_date': DateInput(),
        }
        fields = ['email', 'phone', 'fault', 'booking_type',
                  'booking_date', 'comment']

        comment = forms.CharField(widget=forms.Textarea)

    def clean(self):
        form_booking_date = self.cleaned_data.get('booking_date')
        today = datetime.date.today()
        selected_date_count = Booking.objects.filter(booking_date=form_booking_date).count()

        if selected_date_count >= 5:
            raise forms.ValidationError("Fully booked please select a different day!")

        if form_booking_date <= today:
            raise forms.ValidationError("Please select date in the future!")
        super(BookingForm, self).clean()



from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from PhoneRepairShop.settings import EMAIL_HOST_USER
from django.db.models import F
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .models import PhoneModel, Fault, Booking, BookingType
from .forms import BookingForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Max
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


@staff_member_required
def booking_search_result(request):
    bookings = None
    approved_query = None
    unapproved_query = None
    arrived_query = None
    not_arrived_query = None
    repaired_query = None
    not_repaired_query = None
    collected_query = None
    not_collected_query = None
    post_query = None
    dropoff_query = None
    
    booking_dates_query = None
    booking_query = None
    if 'approve_booking' in request.GET:
        booking_query = request.GET.get('approve_booking')
        approved_query = Booking.objects.all().filter(approve_booking=True, arrived=False, repaired=False, collected=False)
    if 'napprove_booking' in request.GET:
        booking_query = request.GET.get('napprove_booking')
        unapproved_query = Booking.objects.all().filter(approve_booking=False, arrived=False, repaired=False, collected=False)
    if 'arrived' in request.GET:
        booking_query = request.GET.get('arrived')
        arrived_query = Booking.objects.all().filter(approve_booking=True, arrived=True, repaired=False, collected=False)
    if 'not_arrived' in request.GET:
        booking_query = request.GET.get('arrived')
        not_arrived_query = Booking.objects.all().filter(approve_booking=True, arrived=False, repaired=False, collected=False)
    if 'repaired' in request.GET:
        booking_query = request.GET.get('repaired')
        repaired_query = Booking.objects.all().filter(approve_booking=True, arrived=True, repaired=True, collected=False)
    if 'not_repaired' in request.GET:
        booking_query = request.GET.get('repaired')
        not_repaired_query = Booking.objects.all().filter(approve_booking=True, arrived=True, repaired=False, collected=False)
    if 'collected' in request.GET:
        booking_query = request.GET.get('collected')
        collected_query = Booking.objects.all().filter(approve_booking=True, arrived=True, repaired=True, collected=True)
    if 'not_collected' in request.GET:
        booking_query = request.GET.get('collected')
        not_collected_query = Booking.objects.all().filter(approve_booking=True, arrived=True, repaired=True, collected=False)
    
    if 'post' in request.GET:
        booking_query = request.GET.get('booking_type')
        post_query = Booking.objects.all().filter(Q(booking_type__booking_type__icontains='Post'))

    if 'dropoff' in request.GET:
        booking_query = request.GET.get('booking_type')
        post_query = Booking.objects.all().filter(Q(booking_type__booking_type__icontains='Drop off'))

    if 'booking_date' in request.GET:
        booking_query = request.GET.get('booking_date')
        booking_dates_query = Booking.objects.values('booking_date').order_by('booking_date').annotate(max_count=Max('count_bookings'))
    if 'q' in request.GET:
        booking_query = request.GET.get('q')
        bookings = Booking.objects.all().filter(Q(email__icontains=booking_query)
                                                | Q(phone__phone__icontains=booking_query)
                                                | Q(booking_type__booking_type__icontains=booking_query)
                                                | Q(fault__fault__icontains=booking_query))

    return render(request, 'search_booking.html', {'booking_query':booking_query,'approved_query':approved_query,
                                                   'unapproved_query':unapproved_query, 'bookings':bookings,
                                                   'arrived_query':arrived_query,  'not_arrived_query':not_arrived_query,
                                                   'booking_dates_query':booking_dates_query, 'collected_query': collected_query,
                                                   'repaired_query': repaired_query, 'not_repaired_query':not_repaired_query,
                                                   'not_collected_query': not_collected_query, 'post_query':post_query, 
                                                  'dropoff_query':dropoff_query})


class PhoneModelListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PhoneModel
    template_name = 'phone_model.html'

    def test_func(self):
        return self.request.user.is_staff


class PhoneModelCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PhoneModel
    fields = ('phone',)
    template_name = 'phone_new.html'
    success_url = reverse_lazy('booking:phone_model')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@staff_member_required
def phone_remove(self, phone_id):
    phone = PhoneModel.objects.get(id=phone_id)
    phone.delete()
    return redirect('booking:phone_model')


class FaultListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Fault
    template_name = 'faults.html'

    def test_func(self):
        return self.request.user.is_staff


class FaultCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Fault
    fields = ('fault', 'cost')
    template_name = 'fault_new.html'
    success_url = reverse_lazy('booking:faults')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@staff_member_required
def fault_remove(self, fault_id):
    fault = Fault.objects.get(id=fault_id)
    fault.delete()
    return redirect('booking:faults')


class BookingDetailsListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'all_bookings.html'



class ManageBookingDetailsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'manage_bookings.html'

    def test_func(self):
        return self.request.user.is_staff


class BookingApproveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    template_name = 'booking_approve.html'
    fields = ['approve_booking', 'arrived', 'repaired', 'collected']
    success_url = reverse_lazy('booking:manage_bookings')

    def test_func(self):
        return self.request.user.is_staff

@staff_member_required
def email_collection(request, collect_id):
    email_b=None
    booking = Booking.objects.get(id=collect_id)
    Booking.objects.filter(id=collect_id, repaired=True)
    email_b = Booking.objects.values_list('email', flat=True).filter(id=collect_id)
    subject = 'Your device is ready to collect'
    message = 'Your device is repaired and ready to collect.' \
            'Please contact the shop to disscus collection options.'
 
    recepient = email_b[0]
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
    success_message="Collection request Email sent to: " + recepient
    messages.success(request, success_message)

    return redirect('booking:manage_bookings')


@staff_member_required
def refuse_booking(request, refuse_id):
    email_b=None
    booking = Booking.objects.get(id=refuse_id)
    Booking.objects.filter(id=refuse_id).update(refuse=True)
    email_b = Booking.objects.values_list('email', flat=True).filter(id=refuse_id)
    subject = 'Welcome to Phone Parts and Repair Shop'
    message = 'Sorry we can take your booking.' \
                'Please contact the shop to disscuss other alternatives.'
 
    recepient = email_b[0]
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
    success_message="Booking refused - Email sent to: " + recepient
    messages.success(request, success_message)
    booking.delete()
    return redirect('booking:manage_bookings')


class BookingTypeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookingType
    template_name = 'booking_type.html'

    def test_func(self):
        return self.request.user.is_staff


class BookingTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BookingType
    fields = ('booking_type',)
    template_name = 'bookingType_new.html'
    success_url = reverse_lazy('booking:booking_type')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@staff_member_required
def bookingType_remove(self, type_id):
    bookingType = BookingType.objects.get(id=type_id)
    bookingType.delete()
    return redirect('booking:booking_type')

@login_required()
def new_booking(request):
    if request.method == 'POST':
        f = BookingForm(request.POST)
        if f.is_valid():
            new_b = f.save(commit=False)
            new_b.author = request.user
            b_date = new_b.booking_date
            count = Booking.objects.filter(booking_date=b_date).update(count_bookings=F("count_bookings") + 1)
            Booking.objects.filter(booking_date=b_date).update(count_bookings=count+1)
            fault = new_b.fault
            cost = fault.cost
            f.save()
            subject = 'Welcome to Phone Parts and Repair Shop'
            message = 'We received your booking request we will get back to you soon. ' \
                      'You can see your booking details and progress on our website.'
            recepient = str(f['email'].value())
            send_mail(subject,
                      message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            return render(request, 'booking_confirmation.html', {'cost': cost})
    else:
        f = BookingForm()
    return render(request, 'booking_new.html', {'form': f})


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'booking_delete.html'
    success_url = reverse_lazy('booking:all_bookings')
    success_message = 'Your booking was canceled.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BookingDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


@login_required()
def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking_detail.html', {'booking':booking})

from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from .models import Booking, PhoneModel, Fault, BookingType
from accounts.models import CustomUser
from .forms import BookingForm
from django.core.exceptions import ValidationError
from django.urls import reverse
from PhoneRepairShop.settings import EMAIL_HOST_USER
from django.core import mail



class BookingTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='sabinamihoc02@gmail.com',
            password='secret'
        )
        self.admin = CustomUser.objects.create_superuser(
            username='staff', 
            email='staffemail@gmail.com', 
            password='secret')

        self.booking = Booking.objects.create(
            id=1234,
            author = self.user,
            email='sabinamihoc02@gmail.com',
            phone=PhoneModel(phone='iPhone 8'),
            fault=Fault(fault='Audio'),
            booking_type=BookingType(booking_type='Post'),
            booking_date= '2021-04-22',
            comment='test',
        )
        self.phone = PhoneModel.objects.create(
            id=1,
            phone='Samsung'
        )
        self.fault = Fault.objects.create(
            id=2,
            fault='camera front',
            cost=44,
        )
        self.booking_type = BookingType.objects.create(
            id=3,
            booking_type='post test'
        )

    def tearDown(self):
        #self.user.delete()
        self.admin.delete()
        self.booking.delete()
        self.phone.delete()
        self.fault.delete()
        self.booking_type.delete()

    def test_user_login_correct_credentials(self):
        self.user = authenticate(username='testuser', password='secret')
        self.assertTrue((self.user is not None) and self.user.is_authenticated)
        login = self.client.login(username='testuser', password='secret')
        self.assertTrue(login)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_user_login_wrong_username(self):
        self.user = authenticate(username='wrong', password='secret')
        self.assertFalse(self.user is not None and self.user.is_authenticated)

    def test_user_login_wrong_password(self):
        self.user = authenticate(username='testuser', password='wrong')
        self.assertFalse(self.user is not None and self.user.is_authenticated)

    def test_admin_login_successfully(self):
        self.admin = authenticate(username='staff', password='secret')
        self.assertTrue((self.admin is not None) and self.admin.is_authenticated)
        login = self.client.login(username='staff', password='secret')
        self.assertTrue(login)
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
    
    def test_booking_form_valid_as_user_successfully(self):
        login = self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse('booking:booking'))
        self.assertEqual(response.status_code, 200)
        #fill in the form
        form_data = {
                    'email':'sab@gmail.com',
                    'phone':self.phone.id,
                    'fault':self.fault.id,
                    'booking_type':self.booking_type.id,
                    'booking_date':'2021-05-27',
                    'comment':'test comment',
                    }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid()) # check if form is valid
        self.assertFalse(form.errors) # should be no errors
    
    def test_access_booking_form_unregistered_user_fail(self):
        login = self.client.login(username='', password='')
        self.assertFalse(login) # is not logged in
        response=self.client.get(reverse('booking:booking'))
        self.assertEqual(response.status_code, 302) #redirects to login page

    def test_booking_form_invalid_empty_field_fail(self):
        #fill in the form
        form_data = {
                    'email':'sab@gmail.com',
                    'phone':'',  #required field
                    'fault':self.fault.id,
                    'booking_type':self.booking_type.id,
                    'booking_date':'2021-05-27',
                    'comment':'test comment',
                    }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid()) # check if form is invalid
        self.assertTrue(form.errors) #check is error is returned, <li>phone<ul class="errorlist"><li>This field is required.</li>
        response=self.client.get(reverse('booking:booking'))
        self.assertEqual(response.status_code, 302)
    
    def test_booking_form_invalid_date_fail(self):
        #fill in the form
        form_data = {
                    'email':'sab@gmail.com',
                    'phone':self.phone.id,
                    'fault':self.fault.id,
                    'booking_type':self.booking_type.id,
                    'booking_date':'', #invalid
                    'comment':'test comment',
                    }
        form = BookingForm(data=form_data)
        try:
            self.assertFalse(form.is_valid()) # check if form is invalid, should raise an error
        except:
            self.assertTrue(form.errors) #check is error is returned, <li>booking_date<ul class="errorlist"><li>This field is required.</li>
            
    def test_send_email_successfully(self):
        mail.send_mail('TEST EMAIL- Your device is ready to collect', 'Your device is repaired and ready to collect.' \
            'Please contact the shop to disscus collection options.',
            EMAIL_HOST_USER, ['sabinamihoc02@gmail.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'TEST EMAIL- Your device is ready to collect')

    def test_check_booking_details_correct(self):
        self.assertEqual(f'{self.booking.id}', '1234')
        self.assertEqual(f'{self.booking.author}', 'testuser')
        self.assertEqual(f'{self.booking.email}', 'sabinamihoc02@gmail.com')
        self.assertEqual(f'{self.booking.phone}', 'iPhone 8')
        self.assertEqual(f'{self.booking.fault}', 'Audio')
        self.assertEqual(f'{self.booking.booking_type}', 'Post')
        self.assertEqual(f'{self.booking.booking_date}', '2021-04-22')
        self.assertEqual(f'{self.booking.comment}', 'test')
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_check_phone_details_correct(self):
        self.assertEqual(f'{self.phone.id}', '1')
        self.assertEqual(f'{self.phone.phone}', 'Samsung')
        self.assertEqual(PhoneModel.objects.count(), 1)
    
    def test_check_fault_details_correct(self):
        self.assertEqual(f'{self.fault.id}', '2')
        self.assertEqual(f'{self.fault.fault}', 'camera front')
        self.assertEqual(self.fault.cost, 44)
        self.assertEqual(Fault.objects.count(), 1)

    def test_check_booking_type_details_correct(self):
        self.assertEqual(f'{self.booking_type.id}', '3')
        self.assertEqual(f'{self.booking_type.booking_type}', 'post test')
        self.assertEqual(BookingType.objects.count(), 1)

    def test_admin_add_phone_using_form_successfully(self):
        login = self.client.login(username='staff', password='secret')
        #fill in the form
        response=self.client.post(reverse('booking:phone_new'), data={'phone':'newtestphone'})
        self.assertEqual(response.status_code, 302)
        # check if the phone is in the list
        response=self.client.get(reverse('booking:phone_model'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'newtestphone')
        #count the phone obj to check if it saved
        self.assertEqual(PhoneModel.objects.count(), 2)
        # check phone string representation 
        phone = PhoneModel(phone='newtestphone')
        self.assertEqual(str(phone), phone.phone)
    
    def test_admin_add_phone_empty_field_fail(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.post(reverse('booking:phone_new'), data={'phone':''})
        self.assertEqual(PhoneModel.objects.count(), 1)

    def test_user_access_phone_list_forbidden(self):
        login = self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse('booking:phone_model'))
        self.assertEqual(response.status_code, 403) #403: Forbidden error

    def test_admin_delete_phone_successfully(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.get(reverse('booking:phone_model'))
        self.assertEqual(response.status_code, 200)
        phone = PhoneModel.objects.all().filter(phone='newtestphone')
        phone.delete()
        self.assertEqual(PhoneModel.objects.count(), 1)

    def test_admin_add_fault_using_form_successfully(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.post(reverse('booking:fault_new'), data={'fault':'testfault', 'cost':50})
        self.assertEqual(response.status_code, 302)
        response=self.client.get(reverse('booking:faults'))
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'testfault')
        self.assertContains(response, '50')
        self.assertEqual(Fault.objects.count(), 2)
    
    def test_admin_add_fault_invalid_cost_fail(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.post(reverse('booking:fault_new'), data={'fault':'testfault', 'cost':'invalid'})
        self.assertEqual(Fault.objects.count(), 1)
    
    def test_admin_add_fault_empty_field_fail(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.post(reverse('booking:fault_new'), data={'fault':'', 'cost':50})
        self.assertEqual(Fault.objects.count(), 1)
    
    def test_user_access_fault_list_forbidden(self):
        login = self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse('booking:faults'))
        self.assertEqual(response.status_code, 403) #forbidden

    def test_admin_delete_fault_successfully(self):
        login = self.client.login(username='staff', password='secret')
        fault = Fault.objects.all().filter(fault='testfault')
        fault.delete()
        self.assertEqual(Fault.objects.count(), 1)
    
    def test_admin_add_bookingType_successfully(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.post(reverse('booking:bookingType_new'), data={'booking_type':'testtype'})
        self.assertEqual(response.status_code, 302)
        response=self.client.get(reverse('booking:booking_type'))
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'testtype')
        self.assertEqual(BookingType.objects.count(), 2)
    
    def test_admin_add_booking_type_empty_field_fail(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.post(reverse('booking:bookingType_new'), data={'booking_type':''})
        self.assertEqual(BookingType.objects.count(), 1)
    
    def test_user_access_bookingType_list_forbidden(self):
        login = self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse('booking:booking_type'))
        self.assertEqual(response.status_code, 403)
    
    def test_admin_delete_bookingType_successfully(self):
        login = self.client.login(username='staff', password='secret')
        booking_type = BookingType(booking_type='testype')
        self.assertEqual(str(booking_type), booking_type.booking_type)
        booking_type.delete()
        self.assertEqual(BookingType.objects.count(), 1)
    
    def test_access_bookings_interface_admin_successfully(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.get(reverse('booking:manage_bookings'))
        self.assertEqual(response.status_code, 200) #ok
    
    def test_access_bookings_interface_user_forbidden(self):
        login = self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse('booking:manage_bookings'))
        self.assertEqual(response.status_code, 403) #ok

    def test_access_search_booking_page_as_admin_successfully(self):
        login = self.client.login(username='staff', password='secret')
        response=self.client.get(reverse('booking:booking_search_result'))
        self.assertEqual(response.status_code, 200) #ok

    def test_access_search_booking_page_as_user_fail(self):
        login = self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse('booking:booking_search_result'))
        self.assertEqual(response.status_code, 302) # redirect to django admin login page



    '''this doesn't work
    def test_booking_form_fully_booked_successfully(self):
        # 5 bookings per day
        for booking in range(6):
            form_data = {
                    'email':'sab@gmail.com',
                    'phone':self.phone.id,
                    'fault':self.fault.id,
                    'booking_type':self.booking_type.id,
                    'booking_date':'2021-05-19',
                    'comment':'test comment',
                    }
            form = BookingForm(data=form_data)
            self.assertTrue(form.is_valid()) # valid
            if booking == 5:   # after 5 booking no more bookings with same date
                self.assertFalse(form.is_valid()) #invalid
                self.assertTrue(form.errors) # should be an error''' 








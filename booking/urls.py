from django.urls import path

from . import views
from .views import (
    PhoneModelListView,
    FaultListView,
    BookingTypeListView,
    BookingDetailsListView,
    BookingDeleteView,
    BookingApproveUpdateView,
    FaultCreateView,
    ManageBookingDetailsListView,
    BookingTypeCreateView,
    PhoneModelCreateView,
)

app_name='booking'

urlpatterns = [
    path('faultRemove/<uuid:fault_id>/', views.fault_remove, name='fault_remove'),
    path('manageBookings/', ManageBookingDetailsListView.as_view(), name='manage_bookings'),
    path('all_bookings/', BookingDetailsListView.as_view(), name='all_bookings'),
    path('bookingTypeRemove/<uuid:type_id>/', views.bookingType_remove, name='bookingType_remove'),
    path('bookingType/', BookingTypeListView.as_view(), name='booking_type'),
    path('newBookingType/', BookingTypeCreateView.as_view(), name='bookingType_new'),
    path('newFault/', FaultCreateView.as_view(), name='fault_new'),
    path('faults/', FaultListView.as_view(), name='faults'),
    path('PhoneRemove/<uuid:phone_id>/', views.phone_remove, name='phone_remove'),
    path('phoneNew/', PhoneModelCreateView.as_view(), name='phone_new'),
    path('model/', PhoneModelListView.as_view(), name='phone_model'),
    path('<slug:pk>/bookingApprove', BookingApproveUpdateView.as_view(), name='booking_approve'),
    path('<slug:pk>/delete', BookingDeleteView.as_view(), name='booking_delete'),
    path('details/<uuid:booking_id>/', views.booking_detail, name='booking_detail'),
    path('newbooking/', views.new_booking, name='booking'),
    path('collection/<uuid:collect_id>/', views.email_collection, name='email_collection'),
    path('refuse/<uuid:refuse_id>/', views.refuse_booking, name='refuse_booking'),
    path('bookingSearch/', views.booking_search_result, name='booking_search_result'),
]
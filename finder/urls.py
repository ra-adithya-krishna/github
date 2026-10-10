from django.contrib import admin
from django.urls import path
from . import views
from finder.views import view_bookings
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('location/', views.location, name='location'),
    path('maps/', views.maps, name='maps'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('book-slot/', views.bookslot, name='bookslot'),
    path('planning/', views.planning, name='planning'),
    path('review/' , views.station_review , name='review'),
    path('station/<slug:slug>/review/' , views.station_review , name='station_review'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/manage_stations/', views.manage_stations, name='manage_stations'),
    path('admin_dashboard/manage_users/', views.manage_users, name='manage_users'),
    path('admin_dashboard/manage_users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # ✅ Add these for station actions by name
    path('admin_dashboard/edit_station/<str:station_name>/', views.edit_station_by_name, name='edit_station_by_name'),
   path('admin_dashboard/delete_station/<str:station_name>/', views.delete_station_by_name, name='delete_station_by_name'),

# path('station/<slug:slug>/review/', views.station_review, name='station_review'),
#  path('station/<slug:slug>/', views.station_review, name='station_review'),
 
    #path('station/<str:station_name>/review/', views.station_review_by_name, name='review_by_name'),
# urls.py
# path('station/<str:station_name>/review/', views.station_review_by_name, name='station_review_by_name'),





path('admin_dashboard/approve_home_station/<int:station_id>/', views.approve_home_station, name='approve_home_station'),
path('admin_dashboard/reject_home_station/<int:station_id>/', views.reject_home_station, name='reject_home_station'),
 path('admin_dashboard/view_bookings/', view_bookings, name='view_bookings'),
     path('admin_dashboard/user/<int:user_id>/', views.view_user_details, name='view_user_details'),
     
    path('home_register_station/', views.home_register_station, name='home_register_station'),
    
    path('home_register_station/', views.home_register_station, name='home_register_station'),
    path('admin_dashboard/manage_home_stations/', views.manage_home_stations, name='manage_home_stations'),
    path('admin_dashboard/approve_home_station/<int:station_id>/', views.approve_home_station, name='approve_home_station'),
    path('admin_dashboard/reject_home_station/<int:station_id>/', views.reject_home_station, name='reject_home_station'),
     path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('admin_dashboard/delete-home-station/<int:id>/', views.delete_home_station, name='delete_home_station'),
   path('view-booked-slots/', views.view_booked_slots, name='view_booked_slots'),
   path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
   path('homeinterface/', views.homeinterface, name='homeinterface'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),

    
    path('payment/', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('razorpay-payment/', views.razorpay_payment, name='razorpay_payment'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),


     

    

]

from django.shortcuts import render
import mysql.connector
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import render
from .models import ChargingStation
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChargingStation
from django.shortcuts import get_object_or_404, redirect
from .models import ChargingStation
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChargingStation, StationReview
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import ChargingStation
from .models import Booking
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HomeChargingStation
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeStationForm
from .models import ChargingStation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .models import HomeChargingStation
from .forms import HomeStationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChargingStation, HomeChargingStation
from django.shortcuts import redirect, get_object_or_404
from .models import HomeChargingStation
from .models import BookingSlot 

from django.shortcuts import get_object_or_404, render, redirect
from .models import ChargingStation
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.urls import reverse
import razorpay
import json






def location(request):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kerala_ev_charging;")
    stations = cursor.fetchall()
    connection.close()
    return render(request, 'location.html', {'stations': stations})


# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request , 'index.html')


# def location(request):
#     return render(request , 'location.html')


def maps(request):
    return render(request , 'maps.html')

def about(request):
    return render(request , 'about.html')


def contact(request):
    return render(request , 'contact.html')


def register(request):
    error = ''
    success = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already taken."
        elif User.objects.filter(email=email).exists():
            error = "Email already registered."
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            success = "Registration successful! You can now log in."
            return redirect('login')  # Optional: redirect after register

    return render(request, 'register.html', {'error': error, 'success': success})




def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if role == 'admin' and user.is_staff:
                return redirect('admin_dashboard')  # You must have this URL set
            elif role == 'user':
                return redirect('home')  # Redirect to home or user dashboard
            elif role == 'home':
                return redirect('homeinterface') 
            else:
                error = 'You do not have permission for this role.'
        else:
            error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})


@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')  # Non-admins get kicked back to login
    return render(request, 'admin_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def bookslot(request):
    station_name = request.GET.get('name', 'Unknown Station')

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time'] + ' ' + request.POST['ampm']
        duration = request.POST['duration']  # from duration dropdown
        station_name = request.POST['station_name']

        # Calculate amount (you can modify this logic as needed)
        amount = float(duration) * 50  # 50 rupees per hour as example

        # Store booking details in session for payment processing
        request.session['booking_data'] = {
            'user_id': request.user.id,
            'station_name': station_name,
            'date': date,
            'time': time,
            'duration': duration,
            'amount': amount
        }

        # Redirect to payment page
        return redirect('payment')

    return render(request, 'bookslot.html', {
        'station_name': station_name
    })



def planning(request):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kerala_ev_charging;")
    stations = cursor.fetchall()
    connection.close()
    return render(request, 'planning.html', {'stations': stations})

# views.py

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')

    total_stations = ChargingStation.objects.count()
    total_users = User.objects.count() # You can use User.objects.count() if you have users
    total_revenue = 0  # Replace with real calculation if available

    stations = ChargingStation.objects.all()
    home_stations = HomeChargingStation.objects.all()

    return render(request, 'admin_dashboard.html', {
        'total_stations': total_stations,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'stations': stations,
        'home_stations':home_stations
    })
# def manage_stations(request):
#     if request.method == 'POST':
#         name = request.POST.get('station_name')
#         location = request.POST.get('location')
#         owner = request.POST.get('owner')
#         status = request.POST.get('status')
#         contact_info = request.POST.get('contact_info')  # ✅ Add this

#         ChargingStation.objects.create(
#             station_name=name,
#             location=location,
#             owner=owner,
#             status=status,
#             contact_info=contact_info  # ✅ Add this
#         )
#         return redirect('manage_stations')

#     stations = ChargingStation.objects.all()
#     return render(request, 'manage_stations.html', {'stations': stations})

def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')


def manage_stations(request):
    if request.method == 'POST':
        # Get data from form
        name = request.POST.get('station_name')
        location = request.POST.get('location')
        owner = request.POST.get('owner')
        status = request.POST.get('status')
        contact_info = request.POST.get('contact_info')

        # Save to DB
        ChargingStation.objects.create(
            station_name=name,
            location=location,
            owner=owner,
            status=status,
            contact_info=contact_info
        )
        return redirect('manage_stations')

    stations = ChargingStation.objects.all()
    return render(request, 'manage_stations.html', {'stations': stations})

def edit_station_by_name(request, station_name):
    station = get_object_or_404(ChargingStation, station_name=station_name)

    if request.method == 'POST':
        station.station_name = request.POST['station_name']
        station.location = request.POST['location']
        station.status = request.POST['status']
        station.owner = request.POST['owner']
        station.save()
        return redirect('manage_stations')

    return render(request, 'edit_station.html', {'station': station})


def delete_station_by_name(request, station_name):
    station = get_object_or_404(ChargingStation, station_name=station_name)
    station.delete()
    return redirect('manage_stations')

@login_required(login_url='login')

def station_review(request, slug):
    print(slug)
    print(ChargingStation.objects.all().values())
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kerala_ev_charging where id = {};".format(slug))  
    stations = cursor.fetchone()
    connection.close()
    #station = get_object_or_404(ChargingStation, slug=slug)
    print(stations)
    reviews = StationReview.objects.filter(station_name=stations['station_name'])


    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        StationReview.objects.create(
            station_name=stations['station_name'],
            slug=slug,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('station_review', slug=slug)

    return render(request, 'station_review.html', {
        'station': stations,
        'reviews': reviews
    })

def review(request):
    return render(request,'review.html')

# def approve_station(request, station_id):
#     station = get_object_or_404(ChargingStation, id=station_id)
#     station.status = 'Approved'
#     station.save()
#     return redirect('admin_dashboard')


# def reject_station(request, station_id):
#     station = get_object_or_404(ChargingStation, id=station_id)
#     station.status = 'Rejected'
#     station.save()
#     return redirect('admin_dashboard')

@login_required(login_url='login')
def view_bookings(request):
    if not request.user.is_staff:
        return redirect('login')

    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'admin_view_bookings.html', {'bookings': bookings})


def view_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    bookings = Booking.objects.filter(user=user)
    return render(request, 'view_user_details.html', {'user_obj': user, 'bookings': bookings})

@login_required
def home_register_station(request):
    if request.method == 'POST':
        form = HomeStationForm(request.POST)
        #if form.is_valid():
        station_name = request.POST.get('station_name', 'Unknown Station')
        location1 = request.POST.get('location', 'Unknown Location')
        #station = form.save(commit=False)
        #station.user = request.user  # assuming ForeignKey to User
        #station.status = 'Pending'
        #station.save()
        HomeChargingStation.objects.create(
            user = request.user,
            station_name=station_name,
            location=location1,
            rate = request.POST.get('rate' , 0),
            charger_type = request.POST.get('charger_type' , "AC"),
            availability = request.POST.get('availability', "NA"),
            contact = request.POST.get('contact', "NA"),
            description = request.POST.get('description', "NA"),

        )
        messages.success(request, 'Your home charging station request has been submitted for admin approval.')
        #return redirect('home')

    else:
        form = HomeStationForm()
        print("invalid")
    return render(request, 'home_register_station.html', {'form': form})

@staff_member_required(login_url=settings.LOGIN_URL)
def manage_home_stations(request):
    stations = HomeChargingStation.objects.all()
    return render(request, 'admin_manage_home_stations.html', {'home_stations': stations})

@staff_member_required(login_url=settings.LOGIN_URL)
def approve_home_station(request, station_id):
    station = get_object_or_404(HomeChargingStation, id=station_id)
    station.status = 'Approved'
    station.save()
    return redirect('admin_dashboard')


@staff_member_required(login_url=settings.LOGIN_URL)
def reject_home_station(request, station_id):
    print(station_id)
    station = get_object_or_404(HomeChargingStation, id=station_id)
    station.status = 'Rejected'
    station.save()
    return redirect('admin_dashboard')

@login_required
def delete_home_station(request, id):
    if not request.user.is_staff:
        return redirect('login')
    station = get_object_or_404(HomeChargingStation, id=id)
    station.delete()
    return redirect('admin_dashboard')



@login_required
def view_booked_slots(request):
#     booked_slots = BookingSlot.objects.filter(user=request.user)
    booked_slots = Booking.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'view_booked_slots.html', {'booked_slots': booked_slots})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('view_booked_slots')


def homeinterface(request):
    return render(request, 'homeinterface.html')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(StationReview, id=review_id)
    if review.user == request.user or request.user.is_staff:
        slug = review.slug
        review.delete()
        return redirect('station_review', slug=slug)
    else:
        return redirect('station_review', slug=review.slug)
    
@login_required(login_url='login')
def payment_view(request):
    # Get booking data from session
    booking_data = request.session.get('booking_data')
    
    if not booking_data:
        messages.error(request, 'No booking found. Please book a slot first.')
        return redirect('home')
    
    if request.method == 'POST':
        # Get payment details
        card_number = request.POST.get('card_number', '').replace(' ', '')
        expiry_date = request.POST.get('expiry_date', '')
        cvv = request.POST.get('cvv', '')
        cardholder_name = request.POST.get('cardholder_name', '')
        payment_method = request.POST.get('payment_method', 'card')
        
        # Basic validation (fake payment gateway)
        if payment_method == 'card':
            if not (card_number and expiry_date and cvv and cardholder_name):
                messages.error(request, 'Please fill in all card details.')
                return render(request, 'payment.html', {
        'booking_data': booking_data,
        'razorpay_enabled': RAZORPAY_ENABLED
    })
            
            # Simulate card validation (fake)
            if len(card_number) < 16 or len(cvv) < 3:
                messages.error(request, 'Invalid card details. Please check and try again.')
                return render(request, 'payment.html', {
        'booking_data': booking_data,
        'razorpay_enabled': RAZORPAY_ENABLED
    })
        
        # Simulate payment processing delay
        import time
        time.sleep(2)  # 2 second delay to simulate processing
        
        # Simulate payment success (90% success rate for demo)
        import random
        if random.random() < 0.9:
            # Payment successful - save booking to database
            Booking.objects.create(
                user_id=booking_data['user_id'],
                station_name=booking_data['station_name'],
                date=booking_data['date'],
                time=booking_data['time'],
                duration=booking_data['duration']
            )
            
            # Clear session data
            del request.session['booking_data']
            
            messages.success(request, f'Payment successful! Your slot at {booking_data["station_name"]} has been booked.')
            return redirect('payment_success')
        else:
            messages.error(request, 'Payment failed. Please try again with different card details.')
            return render(request, 'payment.html', {
        'booking_data': booking_data,
        'razorpay_enabled': RAZORPAY_ENABLED
    })
    
    return render(request, 'payment.html', {
        'booking_data': booking_data,
        'razorpay_enabled': RAZORPAY_ENABLED
    })

@login_required(login_url='login')
def payment_success(request):
    return render(request, 'payment_success.html')

# Initialize Razorpay client (only if keys are configured)
try:
    if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET and settings.RAZORPAY_KEY_SECRET != 'your_key_secret_here':
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        RAZORPAY_ENABLED = True
    else:
        razorpay_client = None
        RAZORPAY_ENABLED = False
except Exception as e:
    razorpay_client = None
    RAZORPAY_ENABLED = False

@login_required(login_url='login')
def razorpay_payment(request):
    # Check if Razorpay is enabled
    if not RAZORPAY_ENABLED:
        messages.info(request, 'Razorpay is not configured. Please use Demo Payment instead.')
        return redirect('payment')
    
    # Get booking data from session
    booking_data = request.session.get('booking_data')
    
    if not booking_data:
        messages.error(request, 'No booking found. Please book a slot first.')
        return redirect('home')
    
    if request.method == 'POST':
        # Get payment method
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'razorpay':
            # Create Razorpay order
            amount = int(float(booking_data['amount']) * 100)  # Convert to paise
            
            order_data = {
                'amount': amount,
                'currency': 'INR',
                'receipt': f'booking_{request.user.id}_{booking_data["date"]}',
                'notes': {
                    'user_id': request.user.id,
                    'station_name': booking_data['station_name'],
                    'date': booking_data['date'],
                    'time': booking_data['time'],
                    'duration': booking_data['duration']
                }
            }
            
            try:
                order = razorpay_client.order.create(data=order_data)
                
                context = {
                    'booking_data': booking_data,
                    'razorpay_order_id': order['id'],
                    'razorpay_amount': amount,
                    'razorpay_currency': 'INR',
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'user': request.user,
                    'callback_url': request.build_absolute_uri(reverse('razorpay_callback'))
                }
                
                return render(request, 'razorpay_payment.html', context)
                
            except Exception as e:
                messages.error(request, f'Error creating payment order: {str(e)}')
                return render(request, 'payment.html', {
        'booking_data': booking_data,
        'razorpay_enabled': RAZORPAY_ENABLED
    })
        else:
            # Redirect to fake payment for other methods
            return redirect('payment')
    
    return render(request, 'payment.html', {
        'booking_data': booking_data,
        'razorpay_enabled': RAZORPAY_ENABLED
    })

@login_required(login_url='login')
def razorpay_callback(request):
    if request.method == 'POST':
        # Get payment details from Razorpay
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # Verify the payment signature
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Get booking data from session
            booking_data = request.session.get('booking_data')
            
            if booking_data:
                # Payment successful - save booking to database
                Booking.objects.create(
                    user_id=booking_data['user_id'],
                    station_name=booking_data['station_name'],
                    date=booking_data['date'],
                    time=booking_data['time'],
                    duration=booking_data['duration']
                )
                
                # Clear session data
                del request.session['booking_data']
                
                messages.success(request, f'Payment successful! Your slot at {booking_data["station_name"]} has been booked.')
                return redirect('payment_success')
            else:
                messages.error(request, 'Booking data not found.')
                return redirect('home')
                
        except Exception as e:
            messages.error(request, f'Payment verification failed: {str(e)}')
            return redirect('payment_failure')
    
    return redirect('home')

@login_required(login_url='login')
def payment_failure(request):
    return render(request, 'payment_failure.html')
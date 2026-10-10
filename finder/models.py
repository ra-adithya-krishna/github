# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
# from .models import ChargingStation



class ChargingStation(models.Model):
    station_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=255)
    owner = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], default='Pending' )
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_home_station = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.station_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.station_name


class StationReview(models.Model):
    #station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100 , default='')
    slug = models.SlugField(blank=True)
    id = models.IntegerField(primary_key=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station_name} - {self.rating} stars by {self.user.username}"
    

    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=10)
    duration = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.station_name} on {self.date} at {self.time}"
    
    
class HomeChargingStation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    charger_type = models.CharField(max_length=50)
    availability = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station_name} - {self.status}"
    
    # Add this to models.py if required
class BookingSlot(models.Model):
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.station.station_name} | {self.date} {self.start_time}-{self.end_time}"
    


from django import forms
from .models import ChargingStation

class ChargingStationForm(forms.ModelForm):
    class Meta:
        model = ChargingStation
        fields = ['station_name', 'location', 'owner', 'status','contact_info']

        
class HomeStationForm(forms.ModelForm):
    class Meta:
        model = ChargingStation
        fields = ['station_name', 'location', 'hourly_rate', 'contact_info']

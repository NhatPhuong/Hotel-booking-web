# Create your views here.
# Mẫu
from django.shortcuts import render
from .models import RoomType

def index(request):
    rooms = RoomType.objects.all()
    return render(request, 'Hotel-booking-web/Hotel-booking-web/bookings/templates/bookings/index.html')

# Create your views here.
# Mẫu
from django.shortcuts import render
from .models import RoomType

def index(request):
    rooms = RoomType.objects.all()
    return render(request, 'bookings/templates/bookings/index.html', {'rooms': rooms})

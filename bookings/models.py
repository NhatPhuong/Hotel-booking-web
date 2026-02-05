from django.db import models

# Create your models here.
# Mẫu
class RoomType(models.Model):
    name = models.CharField(max_length=100) # Ví dụ: Kingsize, Standard
    price = models.DecimalField(max_digits=10, decimal_places=0)
    total_rooms = models.IntegerField(default=1)
    available_rooms = models.IntegerField(default=1)

    def __str__(self):
        return self.name
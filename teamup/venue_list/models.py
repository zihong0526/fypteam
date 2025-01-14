from django.db import models
from sport_list.models import Sport

class Venue(models.Model):
    name = models.CharField(max_length=255)
    sport_types = models.ManyToManyField(Sport, related_name='venue_list')
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(default='default.jpg', upload_to='venue_images')

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from sport_list.models import Sport


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def get_sport_choices():
        return [(sport.name, sport.name) for sport in Sport.objects.all()]

    SPORT_CHOICES = get_sport_choices()

    # SPORT_CHOICES = (
    #     ('Beginner', 'Beginner'),
    #     ('Medium', 'Medium'),
    #     ('Pro', 'Pro'),
    # )

    SKILL_LEVEL_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Medium', 'Medium'),
        ('Pro', 'Pro'),
    )

    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('SECRET', 'SECRET'),
    )

    sport_1 = models.CharField(max_length=100, choices=SPORT_CHOICES, default='Basketball')
    skill_level_1 = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='Beginner')

    sport_2 = models.CharField(max_length=100, choices=SPORT_CHOICES, default='Football')
    skill_level_2 = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='Beginner')

    sport_3 = models.CharField(max_length=100, choices=SPORT_CHOICES, default='Table Tennis')
    skill_level_3 = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='Beginner')

    location = models.CharField(max_length=100, default='none')
    age = models.PositiveIntegerField(default=18)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


        super().save(*args, **kwargs)



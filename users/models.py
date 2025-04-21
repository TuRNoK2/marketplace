from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    @property
    def is_buyer(self):
        return self.role == 'buyer'

    @property
    def is_seller(self):
        return self.role == 'seller'



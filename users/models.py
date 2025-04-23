from time import timezone

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
    email_confirmed = models.BooleanField(default=False)
    @property
    def is_buyer(self):
        return self.role == 'buyer'

    @property
    def is_seller(self):
        return self.role == 'seller'

    def send_confirmation_email(self):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        token = default_token_generator.make_token(self)
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        confirmation_link = f"{settings.DOMAIN}/confirm-email/{uid}/{token}/"

        send_mail(
            'Подтверждение email',
            f'Для подтверждения email перейдите по ссылке: {confirmation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
        self.confirmation_sent_date = timezone.now()
        self.save()

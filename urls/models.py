from django.db import models
from django.utils import timezone
import shortuuid

from accounts.models import UserData
class URL(models.Model):
    original_url = models.URLField()
    tiny_url = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()
    user = models.ManyToManyField(UserData)

    def save(self, *args, **kwargs):        
        self.expiration_date = timezone.now() + timezone.timedelta(days=7)
        self.tiny_url = shortuuid.uuid()[:8]  # 8 characters of the UUID
        return super().save(*args, **kwargs)
    def is_expired(self):
        return self.expiration_date <= timezone.now() 

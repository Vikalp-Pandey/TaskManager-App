import uuid
from django.db import models
from django.contrib.auth.models import User
import pytz
# Create your models here.
class Task(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    title=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True, blank=True)
    complete=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title) if self.title is not None else f"Task {self.id}"
    
    class Meta:
        ordering=['complete','-created_at']
        # ? By default,  Incompleted Tasks will be returned first,then completed Tasks.
        # ? We can also override it by providing our custom field in queryset.

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    country = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="User's country (e.g., India)"
    )
    timezone = models.CharField(
        max_length=100,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        default='UTC',
        help_text="User's timezone (e.g., Asia/Kolkata for India)"
    )
    
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    


    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s profile ({self.country})"    

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings


class UserProfile(models.Model):
    """
    model to maintain user's delivery
    information and orders.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    user_full_name = models.CharField(max_length=40, null=False, blank=False)
    user_email = models.EmailField(max_length=50, null=False, blank=False)
    user_contact_number = models.CharField(max_length=11,
                                           null=False, blank=False)
    user_address = models.CharField(max_length=60, null=False, blank=False)
    user_postal_code = models.CharField(max_length=10, null=True, blank=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_the_userprofile(sender, instance, created, **kwargs):
    """
    create the user profile and
    save the updated profile if
    already existed
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import  User, Group

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=False)
    description = models.CharField(max_length=500, null=True)
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.name + ', is available:' + self.is_available


class DaySchedule(models.Model):
    date = models.DateField(unique=True)

    emploee_before_12_1 = models.ForeignKey(User, related_name='emploee_before_12_1', on_delete=models.CASCADE)
    emploee_before_12_2 = models.ForeignKey(User, related_name='emploee_before_12_2',  on_delete=models.CASCADE)

    emploee_after_12_1 = models.ForeignKey(User, related_name='emploee_after_12_1',  on_delete=models.CASCADE)
    emploee_after_12_2 = models.ForeignKey(User, related_name='emploee_after_12_2',  on_delete=models.CASCADE)

    # creator = models.ForeignKey(User,  related_name='day_schedule_creator', on_delete=models.CASCADE)

class Receipt(models.Model):
    date = models.DateField()
    creator =  models.ForeignKey(User,  on_delete=models.CASCADE)

class ReceiptItem(models.Model):
    item_id = models.ForeignKey(Item,  on_delete=models.CASCADE)
    receipt_id = models.ForeignKey(Receipt,  on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
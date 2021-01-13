from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField()
    description = models.CharField(max_length=500, null=True)


class DaySchedule(models.Model):
    date = models.DateField(unique=True)

    emploee_before_12_1 = models.CharField(max_length=100)
    emploee_before_12_2 = models.CharField(max_length=100)

    emploee_after_12_1 = models.CharField(max_length=100)
    emploee_after_12_2 = models.CharField(max_length=100)

class Receipt(models.Model):
    date = models.DateField()

class Check_item(models.Model):
    item_id = models.ForeignKey(Item,  on_delete=models.CASCADE)
    receipt_id = models.ForeignKey(Receipt,  on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import User

# Create your models here        .
class Group(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    start_date = models.DateField()
    total_months = models.IntegerField()
#     remaining_months=models.IntegerField()
#     total_due=models.IntegerField()

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()
    user = models.OneToOneField(User)
    
class Subscriptions(models.Model):
    member = models.ForeignKey(Customer)
    group = models.ForeignKey(Group)
    comments = models.CharField(max_length=1000)

class Auction(models.Model):
    subscription = models.ForeignKey(Subscriptions)
    amount = models.IntegerField()
    auction_date = models.DateField()

class Payments(models.Model):
    subscription = models.ForeignKey(Subscriptions)
    amount = models.IntegerField()
    payment_date = models.DateField()

from django.db import models
from django.contrib.auth.models import User

# Create your models here        .
class Group(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    start_date = models.DateField()
    total_months = models.IntegerField()

class Member(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()
    user = models.OneToOneField(User)
    
class Subscriptions(models.Model):
    member = models.ForeignKey(Member)
    group = models.ForeignKey(Group)
    comments = models.CharField(max_length=1000)

class Auction(models.Model):
    group = models.ForeignKey(Group)
    member = models.ForeignKey(Member)
    amount = models.IntegerField()
    auction_date = models.DateField()

class Payments(models.Model):
    group = models.ForeignKey(Group)
    member = models.ForeignKey(Member)
    amount = models.IntegerField()
    payment_date = models.DateField()

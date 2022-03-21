from django.db import models
from django.contrib.auth.models import User

# Create your models here        .
class Group(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    start_date = models.DateField()
    total_months = models.IntegerField()
    commision = models.FloatField()
    started = models.BooleanField(null=True)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()
    user = models.OneToOneField(User, on_delete=models.PROTECT)

class Journal(models.Model):
    member = models.ForeignKey(Customer, null=True, on_delete=models.PROTECT)
    amount = models.IntegerField(null=True)
    entry_date = models.DateField()
    comment = models.CharField(max_length=1000)
    AUCTION = 'A'
    PAYMENT = 'P'
    DISBURSEMENT = 'D'
    ENTRY_TYPES = (
        (AUCTION, 'Auction'),
        (PAYMENT, 'Payment'),
        (DISBURSEMENT, 'Disbursement')
    )
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)

class Subscriptions(models.Model):
    member = models.ForeignKey(Customer, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    comments = models.CharField(max_length=1000)
    auction_amount = models.IntegerField(null=True)
    auction_date = models.DateField(null=True)
    auction_number = models.IntegerField(null=True)
    auction_txn = models.ForeignKey(Journal, on_delete=models.PROTECT, null=True)

class JournalItem(models.Model):
    txn = models.ForeignKey(Journal, on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscriptions, on_delete=models.PROTECT)
    debit = models.IntegerField()
    credit = models.IntegerField()

from django.core.management.base import BaseCommand, CommandError
from chit_main_app.models import Journal, JournalItem
from collections import defaultdict

class Command(BaseCommand):
    help = "Fixes the multiple personal credit entries in each journal"

    def handle(self, *args, **kwargs):
        txn_set = defaultdict(list) 
        
        for ji in JournalItem.objects.all():
            txn_set[ji.txn_id].append(ji)
        for txn_id, ji_list in txn_set.iteritems():
            
            delete_list = []
            add_list = []
            net_change = 0

            if len(ji_list) == 1:
                continue
            for x in ji_list:
                if x.subscription.group.name == 'Personal Credits':
                    delete_list.append(x)
                    net_change += x.credit - x.debit
                if len(delete_list) > 1:
                    new_ji = JournalItem()
                    if(net_change > 0 ):
                        new_ji.credit = net_change
                        new_ji.debit = 0
                    else:
                        new_ji.debit = -net_change
                        new_ji.credit = 0
                    new_ji.subscription = delete_list[0].subscription
                    new_ji.txn = delete_list[0].txn
                    new_ji.save()

                    for x in delete_list:
                        print "Deleting: ", x.id
                        if x.id:
                            x.delete()

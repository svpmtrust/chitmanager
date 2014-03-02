from django.shortcuts import HttpResponse
from django.template import RequestContext, loader
from chit_main_app.models import Group,Customer, Subscriptions, Journal,JournalItem
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
import itertools
from django.db.models import Sum
from datetime import date, datetime
from django.db.models.aggregates import Count

@login_required
def homepage(request):
    if request.user.is_superuser:
        template = 'admin/home.html'
    else:
        template = 'user/home.html'

    return TemplateResponse(request, template)

@login_required
def new_group(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            group_details = Group.objects.get(id=request.GET['id'])
        else:
            group_details = Group()
        template = loader.get_template('groups/new.html')
        context = RequestContext(request, {
                'group_details': group_details
            })
        return HttpResponse(template.render(context))    
    elif request.method == 'POST':
        if 'id' in request.POST:
            group = Group.objects.get(id=request.POST['id'])
        else:
            group = Group()
        group.name = request.POST['groupname']
        group.amount = request.POST['amount']
        group.start_date = request.POST['startdate']
        group.total_months = request.POST['totalmonths']
        group.commision = request.POST['commission']
        group.save()

        return HttpResponseRedirect("/groups/members?id="+str(group.id))

@login_required
def group_list(request):
    group_list = Group.objects.all()
    
    due_amounts = {}
    dues = JournalItem.objects.all().values('subscription__group_id').annotate(Sum('debit'),Sum('credit'))
    for x in dues:
        due_amounts[x['subscription__group_id']] = x['debit__sum'] - x['credit__sum']
        
    auctions_done = {}
    auctions_left = {}
    auction_count = Subscriptions.objects.all().values('group_id').annotate(Count('auction_amount'))
    for x in auction_count:
        auctions_done[x['group_id']] = x['auction_amount__count']
        
    for g in group_list:
        auctions_left[g.id] = g.total_months - auctions_done.get(g.id, 0)
    
    template = loader.get_template('groups/list.html')
    context = RequestContext(request, {
        'group_list': group_list,
        'due_amounts': due_amounts,
        'auctions_left': auctions_left
    })
    return HttpResponse(template.render(context))

@login_required
def group_members(request):
    try:
        member_list = Subscriptions.objects.filter(group_id=request.GET['id'])
        group_details = Group.objects.get(id=request.GET['id'])
        months_done = sum(0 if m.auction_amount is None else 1 for m in member_list)
        remaining_months = group_details.total_months - months_done
        due_amounts = {}
        dues = JournalItem.objects.filter(subscription__group_id=request.GET['id']).values('subscription_id').annotate(Sum('debit'),Sum('credit'))
        for x in dues:
            due_amounts[x['subscription_id']] = x['debit__sum'] - x['credit__sum']
        template = loader.get_template('groups/members.html')
        context = RequestContext(request, {
            'member_list': member_list,
            'group_details':group_details,
            'remaining_months': remaining_months,
            'due_amounts': due_amounts,
            'total_due_amount': sum(due_amounts.values())
        })
        return HttpResponse(template.render(context))        
    except Subscriptions.DoesNotExist:
        return HttpResponse("No members exist in this group.")

@login_required
def delete_group(request):
    group = Group.objects.get(id=request.GET["id"])
    group.delete()
    return HttpResponseRedirect("/groups/list")

@login_required
def new_customer(request):
    if request.method == 'GET':
        context = RequestContext(request)
        template = loader.get_template('customers/new.html')
        return HttpResponse(template.render(context))    
    elif request.method == 'POST':
        username = request.POST['username']
        user = User()
        user.username = username
        user.set_password(username + request.POST['mobile'])
        user.save()
        member_name = request.POST['name'][0].upper()+request.POST['name'][1:]
        member = Customer(name=member_name, mobile_number=request.POST['mobile'])
        member.user = user
        member.save()
        return HttpResponseRedirect("/customers/list")

@login_required
def customer_list(request):
    customer_list = Customer.objects.all().order_by('name')
    due_amounts = {}
    dues = JournalItem.objects.all().values('subscription__member_id').annotate(Sum('debit'),Sum('credit'))
    for x in dues:
        due_amounts[x['subscription__member_id']] = x['debit__sum'] - x['credit__sum']
    
    template = loader.get_template('customers/list.html')
    context = RequestContext(request, {
        'customer_list': customer_list,
        'due_amounts': due_amounts
    })
    return HttpResponse(template.render(context))

@login_required
def delete_customer(request):
    group = Customer.objects.get(id=request.GET["id"])
    group.delete()
    return HttpResponseRedirect("/groups/list")

@login_required
def customershistory(request):
    j = JournalItem.objects.filter(subscription__member_id=request.GET['id']).order_by('txn__entry_date')
    customer_details = Customer.objects.get(id=request.GET['id'])
    c = RequestContext(request, {'journal': j, 'customer_details': customer_details})
    template = loader.get_template('customers/history.html')
    return HttpResponse(template.render(c))

@login_required
def customerstransactions(request):
    context = RequestContext(request)
    template = loader.get_template('customers/transactions.html')
    return HttpResponse(template.render(context))

@login_required
def customersgroups(request): 
    group_list = Subscriptions.objects.filter(member_id=request.GET['id'])
    customer_details = Customer.objects.get(id=request.GET['id'])
    due_amounts = {}
    dues = JournalItem.objects.filter(subscription__member_id=request.GET['id']).values('subscription_id').annotate(Sum('debit'),Sum('credit'))
    for x in dues:
        due_amounts[x['subscription_id']] = x['debit__sum'] - x['credit__sum']
    context = RequestContext(request, {
        'group_list':group_list,
        'customer_details':customer_details,
        'due_amounts': due_amounts,
        'total_due': sum(due_amounts.itervalues())
        })
    template = loader.get_template('customers/grouplist.html')
    return HttpResponse(template.render(context))
    
@login_required
def subscriptionnew(request):
    if request.method == 'GET':
        if 'gid' in request.GET:
            group = Group.objects.get(id=request.GET['gid'])
            customer_list = Customer.objects.all()
            group_list = Group.objects.all()
            template = loader.get_template('customers/subscription.html')
            context = RequestContext(request, {
                'customer_list': customer_list,
                'group_list':group_list,
                'group': group
                })  
            return HttpResponse(template.render(context))
                      
        else:
            customer = Customer.objects.get(id=request.GET['cid'])
            customer_list = Customer.objects.all()
            group_list = Group.objects.all()
            template = loader.get_template('customers/subscription.html')
            context = RequestContext(request, {
                'customer_list': customer_list,
                'group_list':group_list,
                'customer': customer
            })
        return HttpResponse(template.render(context)) 
    elif request.method == 'POST':
        customer_list = request.POST.getlist('to_customer_list')
        group_list = request.POST.getlist('to_group_list')
        for c,g in itertools.product(customer_list, group_list):
            subscription = Subscriptions()
            subscription.group_id = g
            subscription.member_id = c
            subscription.comments = request.POST['comments']
            subscription.save()
        if 'group_id' in request.POST:
            return HttpResponseRedirect('/groups/members?id=' + request.POST['group_id'])
        elif 'customer_id' in request.POST:
            return HttpResponseRedirect('/customers/grouplist?id=' + request.POST['customer_id'])
        else:
            return HttpResponse("We don't know your origin")

@login_required 
def subscriptionslist(request):
    subscription_list = Subscriptions.objects.all()
    template = loader.get_template('subscriptions/list.html')
    context = RequestContext(request, {
        'subscription_list': subscription_list,
        
    })
    return HttpResponse(template.render(context))

@login_required
def new_auction(request):
    if request.method == 'GET':
        group = Group.objects.get(id=request.GET['id'])
        subscriptions_list = Subscriptions.objects.filter(group_id=request.GET['id'])
        subscription_count = Subscriptions.objects.filter(group_id=request.GET['id']).count()
        if subscription_count > group.total_months:
            return HttpResponse("Group Over subscribed")
        elif subscription_count < group.total_months:
            under_subscribed = True
        else:
            under_subscribed = False
        auction_month = sum(0 if s.auction_amount is None else 1 for s in subscriptions_list)+1
        subscriptions_list = filter(lambda s:s.auction_amount is None, subscriptions_list)
        template = loader.get_template('groups/auction.html')
        context = RequestContext(request, {
            'subscriptions_list':subscriptions_list,
            'group':group,
            'auction_month':auction_month,
            'under_subscribed': under_subscribed 
        })
        return HttpResponse(template.render(context))
    elif request.method == 'POST':
        # Mark the subscription for the auction
        s = Subscriptions.objects.get(id=request.POST['auctionmember'])
        s.auction_amount = float(request.POST['amount'])
        s.auction_date = request.POST['date']
        s.auction_number = request.POST['month']
        s.save()
        
        g = s.group
        if not g.started:
            g.started = True
            g.save()
        
        # Add missing subscriptions
        subscription_count = Subscriptions.objects.filter(group_id=g.id).count()
        missing_subscriptions = g.total_months - subscription_count
        if missing_subscriptions > 0:
            for i in range(missing_subscriptions):
                s1 = Subscriptions()
                s1.member_id = 0
                s1.group_id = g.id
                s1.comments = 'Automatically subscribed'
                s1.save()

        monthly_due = g.amount / g.total_months
        dividend = (s.auction_amount - (g.amount * g.commision)/100) / g.total_months
        due_amount = monthly_due - dividend
        
        # Create main journal Entries
        j = Journal()
        j.entry_date = s.auction_date
        j.comments = 'No Comments'
        j.entry_type = j.AUCTION
        j.save()
        
        # Create due amounts after subtracting dividends
        for s1 in Subscriptions.objects.filter(group_id=s.group_id):
            j1 = JournalItem()
            j1.txn = j
            j1.debit = due_amount
            j1.credit = 0
            j1.subscription_id = s1.id
            j1.save()
        
        return HttpResponseRedirect('/groups/members?id='+ request.POST['group_id']) 

@login_required
def record_customer_payment(request):
    payment_amount = int(request.POST['payment_amount'])
    payments_for = {}
    for s in Subscriptions.objects.filter(member_id=request.POST['customer_id']):
        k = 'payment_for_'+str(s.id)
        if k in request.POST and request.POST[k]:
            payments_for[s.id] = int(request.POST[k])
    if sum(payments_for.values()) != payment_amount:
        return HttpResponse('Sum of amounts is not adding up')
    
    j = Journal()
    j.entry_date = datetime.now()
    j.comments = 'No Comments'
    j.entry_type = j.PAYMENT
    j.save()
        
    # Create due amounts after subtracting dividends
    for s_id, p_amount in payments_for.iteritems():
        
        print s_id, p_amount
        
        j1 = JournalItem()
        j1.txn = j
        j1.debit = 0
        j1.credit = p_amount
        j1.subscription_id = s_id
        j1.save()
    
    # Redirect back to the page 
    return HttpResponseRedirect('/customers/grouplist?id='+request.POST['customer_id'])

@login_required
def new_mobile_number(request):
    m = Customer.objects.get(id=request.GET['id'])
    m.mobile_number = request.GET['new_number']
    m.save()
    return HttpResponseRedirect('/customers/list')

@login_required
def remove_subscription(request):
    m = Subscriptions.objects.get(id=request.GET['id'])
    if m:
        m.delete()
    else:
        return HttpResponse('Invalid subscription')
    return_to = request.GET.get('return_to','group')
    if return_to == 'customer':
        return HttpResponseRedirect('/customers/grouplist?id=%s' % m.member_id)
    else:
        return HttpResponseRedirect('/groups/members?id=%s' % m.group_id)

@login_required
def subscription_activity(request):
    j = JournalItem.objects.filter(subscription_id=request.GET['subscription_id']).order_by('txn__entry_date')
    s = Subscriptions.objects.get(id=request.GET['subscription_id'])
    c = RequestContext(request, {'journal': j, 'subscription': s})
    template = loader.get_template('customers/subscription_activity.html')
    return HttpResponse(template.render(c))

@login_required
def change_subscription(request):
    if request.method == 'GET':
        c_list = Customer.objects.all().order_by('name')
        s_details = Subscriptions.objects.get(id=request.GET['id'])
        ctx = RequestContext(request, {'c_list':c_list, 'subscription':s_details})
        template = loader.get_template('groups/change_subscription.html')
        return HttpResponse(template.render(ctx))
    elif request.method == 'POST':
        s_id = request.POST['subscription_id']
        c_id = request.POST['new_subscriber']
        s_details = Subscriptions.objects.get(id=s_id)
        s_details.member_id = c_id
        s_details.save()
        return HttpResponseRedirect('/groups/members?id=%s' % s_details.group_id)

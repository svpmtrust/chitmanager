from django.shortcuts import HttpResponse
from django.template import RequestContext, loader
from chit_main_app.models import Group,Customer, Subscriptions
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
import itertools

@login_required
def homepage(request):
    if request.user.is_superuser:
        template = 'admin/home.html'
    else:
        template = 'user/home.html'

    return TemplateResponse(request, template)

def new_group(request):
    context = RequestContext(request)
    if request.method == 'GET':
        template = loader.get_template('groups/new.html')
        return HttpResponse(template.render(context))    
    elif request.method == 'POST':
        group = Group()
        group.name = request.POST['groupname']
        group.amount = request.POST['amount']
        group.start_date = request.POST['startdate']
        group.total_months = request.POST['totalmonths']
        group.save()
        return HttpResponseRedirect("/groups/list.html")
      
def group_list(request):
    group_list = Group.objects.all()
    template = loader.get_template('groups/list.html')
    context = RequestContext(request, {
        'group_list': group_list,
    })
    return HttpResponse(template.render(context))

def group_members(request):
    try:
        member_list = Subscriptions.objects.filter(group_id=request.GET['id'])
        group_details = Group.objects.get(id=request.GET['id'])
        template = loader.get_template('groups/members.html')
        context = RequestContext(request, {
            'member_list': member_list,
            'group_details':group_details,
              })
        return HttpResponse(template.render(context))        
    except Subscriptions.DoesNotExist:
        return HttpResponse("No members exist in this group.")

def delete_group(request):
    group = Group.objects.get(id=request.GET["id"])
    group.delete()
    return HttpResponseRedirect("/groups/list.html")

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
        member = Customer(name=request.POST['name'], mobile_number=request.POST['mobile'])
        member.user = user
        member.save()
        return HttpResponseRedirect("/customers/list.html")

def customer_list(request):
    customer_list = Customer.objects.all()
    template = loader.get_template('customers/list.html')
    context = RequestContext(request, {
        'customer_list': customer_list,
    })
    return HttpResponse(template.render(context))

def delete_customer(request):
    group = Customer.objects.get(id=request.GET["id"])
    group.delete()
    return HttpResponseRedirect("/groups/list.html")

def customershistory(request):
    group_list = Group.objects.all()
    customer_list = Customer.objects.all()
    context = RequestContext(request, {
        'customer_list': customer_list,
        'group_list':group_list
    })
    template = loader.get_template('customers/history.html')
    return HttpResponse(template.render(context))

def customerstransactions(request):
    context = RequestContext(request)
    template = loader.get_template('customers/transactions.html')
    return HttpResponse(template.render(context))
    
def customersgroups(request): 
    group_list = Subscriptions.objects.filter(member_id=request.GET['id'])
    customer_list = Customer.objects.get(id=request.GET['id'])
    context = RequestContext(request, {
        'group_list':group_list,
        'customer_list':customer_list
        })
    template = loader.get_template('customers/grouplist.html')
    return HttpResponse(template.render(context))
    

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
      
def subscriptionslist(request):
    subscription_list = Subscriptions.objects.all()
    template = loader.get_template('subscriptions/list.html')
    context = RequestContext(request, {
        'subscription_list': subscription_list,
        
    })
    return HttpResponse(template.render(context))


def auctionnew(request):
    if request.method == 'GET':
        group = Group.objects.get(id=request.GET['id'])
        subscriptions_list = Subscriptions.objects.filter(group_id=request.GET['id'])
        auction_month = sum(0 if s.auction_amount is None else 1 for s in subscriptions_list)+1
        subscriptions_list = filter(lambda s:s.auction_amount is None, subscriptions_list)
        template = loader.get_template('auctions/new.html')
        context = RequestContext(request, {
            'subscriptions_list':subscriptions_list,
            'group':group,
            'auction_month':auction_month,
        })
        return HttpResponse(template.render(context))
    elif request.method == 'POST':
        s = Subscriptions.objects.get(id=request.POST['auctionmember'])
        s.auction_amount = request.POST['amount']
        s.auction_date = request.POST['date']
        s.auction_number = request.POST['month']
        s.save()
        return HttpResponseRedirect('/groups/members.html?id='+ request.POST['group_id']) 

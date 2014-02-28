from django.shortcuts import HttpResponse
from django.template import RequestContext, loader
from chit_main_app.models import Group,Customer, Subscriptions,Auction
from django.contrib.auth import authenticate as dj_auth
from django.contrib.auth import logout as dj_logout
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
        template = 'admin/user.html'

    return TemplateResponse(request, template)

def groupsnew(request):
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
      
def groupslist(request):
    group_list = Group.objects.all()
    template = loader.get_template('groups/list.html')
    context = RequestContext(request, {
        'group_list': group_list,
    })
    return HttpResponse(template.render(context))

def memberslist(request):
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

def groupsdelete(request):
    group = Group.objects.get(id=request.GET["id"])
    group.delete()
    return HttpResponseRedirect("/groups/list.html")

def customersnew(request):
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

def customerslist(request):
    customer_list = Customer.objects.all()
    template = loader.get_template('customers/list.html')
    context = RequestContext(request, {
        'customer_list': customer_list,
    })
    return HttpResponse(template.render(context))

def customersdelete(request):
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
            template = loader.get_template('subscriptions/new.html')
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
            template = loader.get_template('subscriptions/new.html')
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
        auction_list = Auction.objects.all()
        group_list = Group.objects.all()
        group = Group.objects.get(id=request.GET['id'])
        subscriptions_list = Subscriptions.objects.filter(group_id=request.GET['id'])
        auction_month = Auction.objects.filter(group_id=request.GET['id']).count() + 1
        template = loader.get_template('auctions/new.html')
        context = RequestContext(request, {
            'auction_list': auction_list,
            'group_list' :group_list,
            'subscriptions_list':subscriptions_list,
            'group':group,
            'auction_month':auction_month,
        })
        return HttpResponse(template.render(context))
    elif request.method == 'POST':
        auction = Auction()
        auction.amount = request.POST['amount']
        auction.auction_date = request.POST['date']
        auction.member_id = request.POST['auctionmember']
        auction.group_id = request.POST['group_id'] 
        auction.month = request.POST['amount']
        auction.save()
        return HttpResponseRedirect('/groups/members.html?id='+ request.POST['group_id']) 



def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/login')

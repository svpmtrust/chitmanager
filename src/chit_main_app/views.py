# from django.shortcuts import render
# from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.template import RequestContext, loader
from chit_main_app.models import Group,Member, Subscriptions,Auction
# from django.shortcuts import render_to_response
from django.contrib.auth import authenticate as dj_auth
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User


# Create your views here.
  
def mygroup(request):
    group_list = Group.objects.all()
    template = loader.get_template('group.html')
    context = RequestContext(request, {
        'group_list': group_list,
    })
    return HttpResponse(template.render(context))


# @login_required(login_url='/login')
def mycustomers(request):
    member_list = Member.objects.all()
    template = loader.get_template('member.html')
    context = RequestContext(request, {
        'member_list': member_list,
    })
    return HttpResponse(template.render(context))

def subscriptions(request):
    subscription_list = Subscriptions.objects.all()
    template = loader.get_template('subscription.html')
    context = RequestContext(request, {
        'subscription_list': subscription_list,
    })
    return HttpResponse(template.render(context))

def auction(request):
    auction_list = Auction.objects.all()
    template = loader.get_template('auction.html')
    context = RequestContext(request, {
        'auction_list': auction_list,
    })
    return HttpResponse(template.render(context))


def login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        user = dj_auth(username=request.POST['username'],
                       password=request.POST['password'])
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    template = loader.get_template('admin.html')
                    return HttpResponse(template.render(context))
                else:
                    template = loader.get_template('user.html')
                    return HttpResponse(template.render(context))
            else:
                context['error'] = 'Your account is disabled'
        else:
            context['error'] = 'Incorrect username or password'
    else:
        context['error'] = None
        
    template = loader.get_template('loginform.html')
    return HttpResponse(template.render(context))

def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/login')

def Customerregistration(request):
    if request.method == 'GET':
        context = RequestContext(request)
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context))    
    elif request.method == 'POST':
        username = request.POST['username']
        user = User()
        user.username = username
        user.set_password(username + request.POST['mobile'])
        user.save()
        member = Member(name=request.POST['name'], mobile_number=request.POST['mobile'])
        member.user = user
        member.save()
        return HttpResponse("/members")

def newcustomer(request):
    context = RequestContext(request)
    template = loader.get_template('register.html')
    return HttpResponse(template.render(context))

def newgroup(request):
    context = RequestContext(request)
    template = loader.get_template('addgroup.html')
    return HttpResponse(template.render(context))

def group(request):
    context = RequestContext(request)
    if request.method == 'GET':
        template = loader.get_template('addgroup.html')
        return HttpResponse(template.render(context))    
    elif request.method == 'POST':
        group = Group()
        group.name = request.POST['groupname']
        group.amount = request.POST['amount']
        group.start_date = request.POST['startdate']
        group.total_months = request.POST['totalmonths']
        group.save()
        return HttpResponseRedirect("/groups")
        
def groupmembers(request):
    context = RequestContext(request)
    if request.method == 'GET':
        template = loader.get_template('subscriptions.html')
    elif request.method == 'POST':
        group = Group()
        member = Member()
        group.name = request.POST['name']
        member.name = request.POST['name']
        subscription = Subscriptions()
        subscription.group = group
        subscription.member = member
        subscription.save()
        return HttpResponseRedirect('/groups')

def subscriptionnew(request):
    member_list = Member.objects.all()
    group_list = Group.objects.all()
    template = loader.get_template('subscriptions/new.html')
    context = RequestContext(request, {
        'member_list': member_list,
        'group_list':group_list,
    })
    return HttpResponse(template.render(context)) 

                    

        

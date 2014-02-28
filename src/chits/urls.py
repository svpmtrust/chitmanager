from django.conf.urls import patterns, url
# from django.contrib import admin
import chit_main_app.views
from django.views.generic.base import RedirectView
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/home')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^home/$', chit_main_app.views.homepage),
     url(r'^groups/new', chit_main_app.views.groupsnew),
    url(r'^groups/list', chit_main_app.views.groupslist),
    url(r'^groups/delete', chit_main_app.views.groupsdelete),
    url(r'^groups/members', chit_main_app.views.memberslist),
    url(r'^customers/new', chit_main_app.views.customersnew),
    url(r'^customers/list', chit_main_app.views.customerslist),
    url(r'^customers/delete', chit_main_app.views.customersdelete),
    url(r'^customers/grouplist', chit_main_app.views.customersgroups),
    url(r'^subscriptions/new', chit_main_app.views.subscriptionnew),
    url(r'^auctions/new', chit_main_app.views.auctionnew),
    url(r'^customers/history', chit_main_app.views.customershistory),
    url(r'^customers/transactions', chit_main_app.views.customerstransactions),
    url(r'^subscriptions/list', chit_main_app.views.subscriptionslist),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)


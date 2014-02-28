from django.conf.urls import patterns, url
import chit_main_app.views
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Basic Stuff
    url(r'^$', RedirectView.as_view(url='/home')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^home/$', chit_main_app.views.homepage),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    
    # Group operations
    url(r'^groups/new$', chit_main_app.views.new_group),
    url(r'^groups/list$', chit_main_app.views.group_list),
    url(r'^groups/delete$', chit_main_app.views.delete_group),
    url(r'^groups/members$', chit_main_app.views.group_members),
    url(r'^groups/auction$', chit_main_app.views.auctionnew),
    
    # Customer Operations
    url(r'^customers/new$', chit_main_app.views.new_customer),
    url(r'^customers/list$', chit_main_app.views.customer_list),
    url(r'^customers/delete$', chit_main_app.views.delete_customer),
    url(r'^customers/grouplist$', chit_main_app.views.customersgroups),
    url(r'^customers/history$', chit_main_app.views.customershistory),
    url(r'^customers/transactions$', chit_main_app.views.customerstransactions),    
    url(r'^customers/subscription$', chit_main_app.views.subscriptionnew),
)

from django.conf.urls import url
import chit_main_app.views
from django.views.generic.base import RedirectView
import django.contrib.auth.views as auth_views

urlpatterns = [
    # Basic Stuff
    url(r'^$', RedirectView.as_view(url='/home')),
    url(r'^login/$', auth_views.login),
    url(r'^home/$', chit_main_app.views.homepage),
    url(r'^logout/$', auth_views.logout, name='logout'),

    # Group operations
    url(r'^groups/new$', chit_main_app.views.new_group),
    url(r'^groups/list$', chit_main_app.views.group_list),
    url(r'^groups/delete$', chit_main_app.views.delete_group),
    url(r'^groups/members$', chit_main_app.views.group_members),
    url(r'^groups/auction$', chit_main_app.views.new_auction),
    url(r'^groups/remove_subscription$', chit_main_app.views.remove_subscription),
    #url(r'^cutomers/grouplist...../remove_loan$', chit_main_app.views.remove_loan),
    url(r'^groups/change_subscription$', chit_main_app.views.change_subscription),
    url(r'^groups/auction_date$', chit_main_app.views.new_auction_date),

    # Customer Operations
    url(r'^customers/new$', chit_main_app.views.new_customer),
    url(r'^customers/remove_loan$', chit_main_app.views.remove_loan),
    url(r'^customers/list$', chit_main_app.views.customer_list),
    url(r'^customers/delete$', chit_main_app.views.delete_customer),
    url(r'^customers/grouplist$', chit_main_app.views.customersgroups),
    url(r'^customers/history$', chit_main_app.views.customershistory),
    url(r'^customers/subscription$', chit_main_app.views.subscriptionnew),
    url(r'^customers/record_payment$', chit_main_app.views.record_customer_payment),
    url(r'^customers/record_loan_payment$', chit_main_app.views.record_customer_loan_payment),
    url(r'^customers/loan_registration$', chit_main_app.views.new_loan),
    url(r'^customers/mobile_number$', chit_main_app.views.new_mobile_number),
    url(r'^customers/name$', chit_main_app.views.new_name),
    url(r'^customers/group_activity$', chit_main_app.views.subscription_activity),
    url(r'^customers/daily_collection$', chit_main_app.views.daily_collection),
    url(r'^customers/delete_payment$', chit_main_app.views.delete_payment),
]

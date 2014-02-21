from django.conf.urls import patterns, url
# from django.contrib import admin
import chit_main_app.views
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^groups/', chit_main_app.views.mygroup),
    url(r'^mycustomers', chit_main_app.views.mycustomers),
    url(r'^subscriptions', chit_main_app.views.subscriptions),
    url(r'^auctions', chit_main_app.views.auction),
    #url(r'^login', chit_main_app.views.login),
    #url(r'^logout', chit_main_app.views.logout),
    url(r'^Customerregistration', chit_main_app.views.Customerregistration),
    url(r'^newcustomer', chit_main_app.views.newcustomer),
    url(r'^newgroup', chit_main_app.views.newgroup),
    url(r'^groupmembers', chit_main_app.views.groupmembers),
    url(r'^group', chit_main_app.views.group),
    url(r'^subscriptionnew', chit_main_app.views.subscriptionnew),
)


from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^post/$', views.post, name='post'),
    url(r'^add_entry/$', views.add_entry, name='add_entry'),
    url(r'^add_comment/$', views.add_comment, name='add_comment'),
    url(r'^register/$', views.register, name='register'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^is_user/$', views.is_user, name='is_user'),
    url(r'^entry/(?P<entry_id>[0-9]+)/$', views.entry, name='entry'),
   ]
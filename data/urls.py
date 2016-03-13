from django.conf.urls import url

from . import views


urlpatterns = [url(r'^(?P<organization>[0-9]*)/$', views.dashboard, name='dashboard'),
               url(r'^(?P<organization>[0-9]*)/master-data$', views.master_data, name='master_data'),
               url(r'^(?P<organization>[0-9]*)/custom-data$', views.custom_data, name='custom_data'),
               url(r'^(?P<organization>[0-9]*)/view-members', views.view_members, name='view_members'),
               url(r'^(?P<organization>[0-9]*)/segment', views.segment, name='segment'),
               url(r'^(?P<organization>[0-9]*)/code-lookup', views.code_lookup, name='code_lookup'),
               ]

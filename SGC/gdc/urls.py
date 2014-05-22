from django.conf.urls import patterns, url
from gdc import views

urlpatterns = patterns('',
    url(r'gdc/list_requests/$', views.list_requests, name='list_requests'),
    url(r'gdc/list_requests/visualize_request/(?P<id_request>\d+)/$', views.visualize_request, name='visualize_request'),
    url(r'gdc/create_request/(?P<id_item>\d+)/$', views.create_request, name='create_request'),
    #url(r'gdc/accept_request/(?P<id_request>\d+)/$', views.accept_request, name='accept_request'),
    #url(r'gdc/reject_request/(?P<id_request>\d+)/$', views.reject_request, name='reject_request'),
)
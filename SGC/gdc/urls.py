from django.conf.urls import patterns, url
from gdc import views

urlpatterns = patterns('',
    url(r'gdc/list_requests/$', views.list_requests, name='list_requests'),
    url(r'gdc/list_requests/visualize_request/(?P<id_request>\d+)/$', views.visualize_request, name='visualize_request'),
    url(r'gdc/create_request/(?P<id_item>\d+)/$', views.create_request, name='create_request'),
    url(r'gdc/accept_request/(?P<id_request>\d+)/$', views.accept_request, name='accept_request'),
    url(r'gdc/reject_request/(?P<id_request>\d+)/$', views.reject_request, name='reject_request'),
    url(r'gdc/list_pending/$', views.list_pending, name='list_pending'),
    url(r'gdc/modify_pending_item/(?P<id_item>\d+)/$', views.modify_pending_item, name='modify_pending_item'),
    url(r'gdc/list_pending_attr/(?P<id_item>\d+)/$', views.list_pending_attr, name='list_pending_attr'),
    url(r'gdc/set_pending_attr_value/(?P<id_attr>\d+)/$', views.set_pending_attr_value, name='set_pending_attr_value'),
    url(r'gdc/list_pending_predecessors/(?P<id_item>\d+)/$', views.list_pending_predecessors, name='list_pending_predecessors'),
    url(r'gdc/set_pending_predecessor/(?P<id_item>\d+)/to/(?P<id_pred>\d+)/$', views.set_pending_predecessor, name='set_pending_predecessor'),
    url(r'gdc/unset_pending_predecessor/(?P<id_item>\d+)/$', views.unset_pending_predecessor, name='unset_pending_predecessor'),
)
from django.conf.urls import patterns, url
from des import views

urlpatterns = patterns('',
    url(r'des/list_attribute_types/$', views.list_attribute_types, name='list_attribute_types'),
    url(r'des/list_attribute_types/create_attribute_type/$', views.create_attribute_type, name='create_attribute_type'),
    #url(r'des/list_attribute_types/modify_attribute_type/(?P<id_attr_type>\d+)$', views.modify_attribute_type, name='modify_attribute_type'),
    #url(r'des/list_attribute_types/delete_attribute_type/(?P<id_attr_type>\d+)$', views.delete_attribute_type, name='delete_attribute_type'),
)
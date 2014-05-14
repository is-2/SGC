from django.conf.urls import patterns, url
from des import views

urlpatterns = patterns('',
    url(r'des/list_attribute_types/$', views.list_attribute_types, name='list_attribute_types'),
    url(r'des/list_attribute_types/create_attribute_type/$', views.create_attribute_type, name='create_attribute_type'),
    url(r'des/list_attribute_types/modify_attribute_type/(?P<id_attribute_type>\d+)/$', views.modify_attribute_type, name='modify_attribute_type'),
    url(r'des/list_attribute_types/delete_attribute_type/(?P<id_attribute_type>\d+)/$', views.delete_attribute_type, name='delete_attribute_type'),
    url(r'des/list_attribute_types/visualize_attribute_type/(?P<id_attribute_type>\d+)/$', views.visualize_attribute_type, name='visualize_attribute_type'),
    url(r'des/list_item_types/$', views.list_item_types, name='list_item_types'),
    url(r'des/list_item_types/create_item_type/$', views.create_item_type, name='create_item_type'),
    url(r'des/list_item_types/modify_item_type/(?P<id_item_type>\d+)/$', views.modify_item_type, name='modify_item_type'),
    url(r'des/list_item_types/delete_item_type/(?P<id_item_type>\d+)/$', views.delete_item_type, name='delete_item_type'),
    url(r'des/list_item_types/visualize_item_type/(?P<id_item_type>\d+)/$', views.visualize_item_type, name='visualize_item_type'),
    url(r'des/list_item_types/assign_attribute_type/(?P<id_item_type>\d+)/$', views.assign_attribute_type, name='assign_attribute_type'),
    url(r'des/list_item_types/assign_attribute_type/(?P<id_item_type>\d+)/grant_attribute_type/(?P<id_attr_type>\d+)/$', views.grant_attribute_type, name='grant_attribute_type'),
    url(r'des/list_item_types/assign_attribute_type/(?P<id_item_type>\d+)/deny_attribute_type/(?P<id_attr_type>\d+)/$', views.deny_attribute_type, name='deny_attribute_type'),
    url(r'des/list_items/$', views.list_items, name='list_items'),
    url(r'des/list_items/create_item/$', views.create_item, name='create_item'),
    url(r'des/list_items/modify_item/(?P<id_item>\d+)/$', views.modify_item, name='modify_item'),
    url(r'des/list_items/delete_item/(?P<id_item>\d+)/$', views.delete_item, name='delete_item'),
    url(r'des/list_items/assign_item_type/(?P<id_item>\d+)/$', views.assign_item_type, name='assign_item_type'),
    url(r'des/list_items/assign_item_type/(?P<id_item>\d+)/add_item_type/(?P<id_item_type>\d+)/$', views.add_item_type, name='add_item_type'),
    url(r'des/list_items/item_history/(?P<id_item>\d+)/$', views.item_history, name='item_history'),
    url(r'des/list_items/item_history/(?P<id_item>\d+)/revert_item/(?P<id_version>\d+)/$', views.revert_item, name='revert_item'),
    url(r'des/list_items/list_attributes/(?P<id_item>\d+)/$', views.list_attributes, name='list_attributes'),
    url(r'des/list_items/list_attributes/(?P<id_item>\d+)/set_attribute_value/(?P<id_attr>\d+)/$', views.set_attribute_value, name='set_attribute_value'),

)
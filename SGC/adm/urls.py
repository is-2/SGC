from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
    url(r'^adm/list_users/$', views.list_users_view, name='list_users'),
    url(r'^adm/list_users/add_user/$', views.add_user_view, name='add_user'),
    url(r'^adm/list_users/mod_user/(?P<id_user>.*)/$', views.mod_user_view, name='mod_user'),
    url(r'^adm/list_users/del_user/(?P<id_user>.*)/$', views.del_user_view, name='del_user'),
    url(r'^adm/list_users/visualize_user/(?P<id_user>.*)/$', views.visualize_user_view, name='vis_user'),
    url(r'^adm/list_users/user_role/(?P<id_user>.*)/$', views.user_role_view, name="user_role"),
    url(r'^adm/list_users/user_role/list_role/(?P<id_user>.*)/$', views.list_role_view, name="list_role"),
    url(r'^adm/list_users/user_role/list_role/grant_role/(?P<id_user>.*)/(?P<id_role>.*)/$', views.grant_role_view, name="grant_role"),
    url(r'^adm/list_users/user_role/deny_role/(?P<id_user>.*)/(?P<id_role>.*)/$', views.deny_role_view, name="deny_role"),
    url(r'^adm/all_roles/$', views.all_roles_view, name="all_roles"),
    url(r'^adm/all_roles/add_role/$', views.add_role_view, name="add_role"),
    url(r'^adm/all_roles/mod_role/(?P<id_role>.*)/$', views.mod_role_view, name="mod_role"),
    url(r'^adm/all_roles/del_role/(?P<id_role>.*)/$', views.del_role_view, name="del_role"),
    url(r'^adm/all_roles/visualize_role/(?P<id_role>.*)/$', views.visualize_role_view, name="vis_role"),
    url(r'^adm/all_roles/role_permission/(?P<id_role>.*)/$', views.role_permission_view, name="role_permission"),
    url(r'^adm/all_roles/role_permission/list_permission/(?P<id_role>.*)/$', views.list_permission_view, name="list_permission"),    
    url(r'^adm/all_roles/role_permission/list_permission/grant_permission/(?P<id_role>.*)/(?P<id_permission>.*)/$', views.grant_permission_view, name="grant_permission"),
    url(r'^adm/all_roles/role_permission/deny_permission/(?P<id_role>.*)/(?P<id_permission>.*)/$', views.deny_permission_view, name="deny_permission"),    
)
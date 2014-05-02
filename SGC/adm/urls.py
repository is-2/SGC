from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
    url(r'^adm/list_users/$', views.list_users, name='list_users'),
    url(r'^adm/list_users/add_user/$', views.add_user, name='add_user'),
    url(r'^adm/list_users/modify_user/(?P<id_user>\d+)/$', views.modify_user, name='modify_user'),
    url(r'^adm/list_users/delete_user/(?P<id_user>\d+)/$', views.delete_user, name='delete_user'),
    url(r'^adm/list_users/visualize_user/(?P<id_user>\d+)/$', views.visualize_user, name='visualize_user'),
    url(r'^adm/list_users/assign_user_groups/(?P<id_user>\d+)/$', views.assign_user_groups, name='assign_user_groups'),
    url(r'^adm/list_users/assign_user_groups/(?P<id_user>\d+)/grant_user_group/(?P<id_group>\d+)/$', views.grant_user_group, name='grant_user_group'),
    url(r'^adm/list_users/assign_user_groups/(?P<id_user>\d+)/deny_user_group/(?P<id_group>\d+)/$', views.deny_user_group, name='deny_user_group'),
    url(r'^adm/list_groups/$', views.list_groups, name='list_groups'),
    url(r'^adm/list_groups/create_group/$', views.create_group, name='create_group'),
    url(r'^adm/list_groups/modify_group/(?P<id_group>\d+)/$', views.modify_group, name='modify_group'),
    url(r'^adm/list_groups/delete_group/(?P<id_group>\d+)/$', views.delete_group, name='delete_group'),
    url(r'^adm/list_groups/assign_perm/(?P<id_group>\d+)/$', views.assign_permissions, name='assign_perm'),
    url(r'^adm/list_groups/assign_perm/(?P<id_group>\d+)/grant_perm/(?P<id_perm>\d+)$', views.grant_permissions, name='grant_perm'),
    url(r'^adm/list_groups/assign_perm/(?P<id_group>\d+)/deny_perm/(?P<id_perm>\d+)$', views.deny_permissions, name='deny_perm'),
    url(r'^adm/list_projects/$', views.list_projects, name='list_projects'),
    url(r'^adm/list_projects/create_project/$', views.create_project, name='create_project'),
    url(r'^adm/list_projects/modify_project/(?P<id_project>\d+)/$', views.modify_project, name='modify_project'),
    url(r'^adm/list_projects/delete_project/(?P<id_project>\d+)/$', views.delete_project, name='delete_project'),
)
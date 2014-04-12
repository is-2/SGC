from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
    url(r'^adm/list_users/$', views.list_users_view, name='list_users'),
    url(r'^adm/add_user/$', views.add_user_view, name='add_user'),
    url(r'^adm/mod_user/(?P<user_id>.*)/$', views.mod_user_view, name='mod_user'),
    url(r'^adm/del_user/(?P<user_id>.*)/$', views.del_user_view, name='del_user'),
)
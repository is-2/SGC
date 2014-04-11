from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
    url(r'^adm/list_users/$', views.list_users_view, name='list_users'),
    url(r'^adm/user/add/$', views.add_user_view, name='add_user'),
)
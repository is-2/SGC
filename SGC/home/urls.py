from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^denied_access/$', TemplateView.as_view(template_name='denied_access.html'), name = 'denied_access'),
)
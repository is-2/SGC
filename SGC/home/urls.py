from django.conf.urls import patterns, url
from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$',views.log_out,name='log_out'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
)
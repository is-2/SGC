from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
    url(r'^add/product/$', views.add_product_view, name='add_product'),
    
    #REAL URLS
    
    url(r'^adm/user/add/$', views.add_user_view, name='add_user'),
)
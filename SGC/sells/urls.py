from django.conf.urls import patterns, url
from sells import views
urlpatterns = patterns('',
    url(r'^add/product/$', views.add_product_view, name='add_product'),
)
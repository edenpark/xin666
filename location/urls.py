from django.conf.urls import url
from .views import index, place_index, categorise_post, post_list, analytics

urlpatterns = [
    url(r'^$', index, name = "index"),
    url(r'analytics$', analytics, name = "analytics"),
    url(r'^location/(?P<place_id>[0-9]+)/(page/(?P<page_num>[0-9]+)/)?$', place_index, name="place_index"),
    # url(r'^location/(?P<place_id>[0-9]+)categorise_post/categorise/new/$', new_post, name="new_post"),
    url(r'^location/(?P<place_id>[0-9]+)/categorise(?:/(?P<post_id>[0-9]+))?/$', 
    	categorise_post, name="categorise_post"),
    url(r'^list$', post_list, name='post_list'),
]

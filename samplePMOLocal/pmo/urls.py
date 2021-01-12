from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/pmo$', views.pmo_list),
    url(r'^api/pmo/(?P<pk>[0-9]+)$', views.pmo_detail),
]
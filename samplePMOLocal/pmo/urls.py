from django.conf.urls import url
from . import views

urlpatterns = [
    url('api/task_list$', views.task_list),
    url('api/task/(?P<pk>[0-9]+)$', views.task_detail),
    url('api/developer_list$', views.developer_list),
    url('api/developer/(?P<pk>[0-9]+)$', views.developer_detail),
    url('api/permission/(?P<pk>[0-9]+)$', views.user_permission),
    url('users/', views.UserList.as_view()),
    url('users/<int:pk>/', views.UserDetail.as_view()),
]
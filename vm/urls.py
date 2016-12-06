from django.conf.urls import url
from vm import views

urlpatterns = [
    url(r'^instance/$', views.instance_list, name='instance_list'),
    url(r'^instance/add/$', views.instance_create, name='instance_create'),
    url(r'^instance/op/$', views.instance_operation, name='instance_operation'),
    url(r'^instance/download/(?P<sshkey_path>\w+)/$', views.download, name='download'),
    url(r'^instance/error/$', views.error, name='error'),
]

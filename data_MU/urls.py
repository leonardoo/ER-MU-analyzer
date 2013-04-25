from django.conf.urls import *

urlpatterns = patterns('data_MU.views',
    url(r'^add/','add_datauser',name='add_data_user'),
    url(r'^view/','view_data_mu',name='view_data_user'),
)
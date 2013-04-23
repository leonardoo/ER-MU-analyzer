from django.conf.urls.defaults import *

urlpatterns = patterns('data_MU.views',
    url(r'^add/','add_datauser',name='add_data_user'),
)
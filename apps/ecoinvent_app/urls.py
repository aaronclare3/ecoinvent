from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginpage),
    url(r'^processregister$', views.register),
    url(r'^process_login$', views.processlogin),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^xml$', views.handle_xml),
    url(r'^filterData$', views.filterData),
    url(r'^seeData/(?P<datasetId>\d+)$', views.seeData),
    url(r'^resetData$', views.resetData),
    url(r'^delete/(?P<datasetId>\d+)$', views.deleteDataset),

]
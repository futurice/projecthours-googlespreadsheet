from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.fetch_data, name='fetch_data'),
]

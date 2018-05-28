from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^home/', views.enter, name = 'home'),
    url(r'^system/', views.system, name = 'system'),
]

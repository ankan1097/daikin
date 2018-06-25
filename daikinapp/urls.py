from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^home/', views.enter, name = 'home'),
    url(r'^system/', views.system, name = 'system'),
    url(r'^senotif/', views.senotif, name = 'senotif'),
    url(r'^acceptance/', views.acceptance, name = 'acceptance'),
    url(r'^custdata/', views.custdata, name = 'custdata'),
    url(r'^rejection/', views.rejection, name = 'rejection'),
    url(r'^search/', views.search, name = 'search'),
    url(r'^mapdata/', views.mapdata, name = 'mapdata'),
    url(r'^dsystem/', views.dsystem, name = 'dsystem'),
    url(r'^chatstart/', views.chatstart, name = 'chatstart'),
    url(r'^chat/', views.chat, name = 'chat'),
    url(r'^chatrefresh/', views.chatrefresh, name = 'chatrefresh'),
    url(r'^feedback/', views.feedback, name = 'feedback'),
    url(r'^realtime/', views.realtime, name = 'realtime'),
    url(r'^report/', views.report, name = 'report'),
]

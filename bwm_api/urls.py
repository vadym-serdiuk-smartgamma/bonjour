from django.urls import path
from bwm_api import views

urlpatterns = [
    path(r'^api/user/(?P<user_id>\d+)/$', views.user_info),
    path(r'^api/user/(?P<user_id>\d+)/recommendations/$', views.user_recommend_genre)
]

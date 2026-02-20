from django.conf.urls import url
from .views import HomeView,StatusView,SignUpView,CustomLoginView,CustomLogoutView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'), 
    url(r'^status/$', StatusView.as_view(), name='status'),  
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', CustomLoginView.as_view(), name='login'),
    url(r'^logout/$', CustomLogoutView.as_view(), name='logout'),
]

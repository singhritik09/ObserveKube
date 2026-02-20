from django.conf.urls import url
from .views import HomeView,StatusView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'), 
    url(r'^status/$', StatusView.as_view(), name='status'),  
]
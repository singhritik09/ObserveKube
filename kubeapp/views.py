# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth .views import LoginView,LogoutView
from forms import SignupForm
# Create your views here.


class HomeView(View):
    template="home.html"
        # context={}
        # return render(request,template,context)
    def get(self,request):
        return render(request,self.template)
class StatusView(View):
    def get(self,request):    
        return HttpResponse("Status is OK")
    

class SignUpView(CreateView):
    form_class=SignupForm
    template_name='signup.html'
    success_url=reverse_lazy('home')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')    
    
    
    
"""in class-based views, URLs are loaded at import time.
If you use:
success_url = reverse('home')
It may fail because URL configuration isn't loaded yet."""
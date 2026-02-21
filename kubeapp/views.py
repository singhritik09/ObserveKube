# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth .views import LoginView,LogoutView
from forms import SignupForm

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from kube_main import overall_dashboard

class HomeView(LoginRequiredMixin,View):
    
    login_url=reverse_lazy('login')
    def get(self,request):    
        template="home.html"
        context={}
        return render(request,template,{})

class StatusView(LoginRequiredMixin,View):
    login_url=reverse_lazy('login')
    def get(self,request):    
        
        running_pods,issue_pods,totalpods,issue_pod_logs = overall_dashboard()

        running_percent = (len(running_pods) * 100.0) / totalpods if totalpods else 0
        issue_percent = (len(issue_pods) * 100.0) / totalpods if totalpods else 0
        context={
            'running_pods': running_pods,
            'issue_pods': issue_pods,
            'totalpods': totalpods,
            'issue_pod_logs': issue_pod_logs,
            'running_percent': running_percent,
            'issue_percent': issue_percent
        }

        template="status.html"
        return render(request,template,context)        
    

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
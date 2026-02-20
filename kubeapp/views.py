# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.

class HomeView(View):
    
    def get(self,request):    
        template="home.html"
        context={}
        return render(request,template,context)
    
class StatusView(View):
    def get(self,request):    
        return HttpResponse("Status is OK")
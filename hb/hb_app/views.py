from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class TestView(View):

    def get(self, *args, **kwargs):
        return HttpResponse("Hello World")
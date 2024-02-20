from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy

# Create your views here.
class HomePageView(TemplateView):
    template_name = "frontend/index.html"

class LoginPageView(TemplateView):
    template_name = "backend/login.html"
class RegisterPageView(TemplateView):
    template_name = "backend/register.html"
class DashboardPageView(TemplateView):
    template_name = "backend/dashboard.html"
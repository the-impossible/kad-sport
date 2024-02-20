from django.urls import path
from sport_app.views import *

app_name = "app"


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login', LoginPageView.as_view(), name='login'),
    path('register', RegisterPageView.as_view(), name='register'),
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
]
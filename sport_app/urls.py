from django.urls import path
from sport_app.views import *

app_name = "app"


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
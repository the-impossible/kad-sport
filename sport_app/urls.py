from django.urls import path
from sport_app.views import *

app_name = "app"


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    # Auth
    path('login', LoginPageView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterPageView.as_view(), name='register'),
    # Dashboard
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
    # Screening
    path('apply_screening', ApplyScreeningPageView.as_view(), name='apply_screening'),
    path('screening_status', ScreeningStatusPageView.as_view(), name='screening_status'),
    # Admin
    path('create_admin', CreateAdminPageView.as_view(), name='create_admin'),
    path('manage_admin', ManageAdminPageView.as_view(), name='manage_admin'),
    path('edit_admin/<str:pk>', EditAdminView.as_view(), name='edit_admin'),
    path('auth/delete_admin/<str:pk>', DeleteAdminView.as_view(), name='delete_admin'),

    path('apply_candidate', ApplyCandidateForScreeningPageView.as_view(), name='apply_candidate'),
    path('manage_candidate', ManageCandidateScreeningPageView.as_view(), name='manage_candidate'),
    path('edit_candidate/<str:pk>', EditCandidateScreeningView.as_view(), name='edit_candidate'),
    path('delete_candidate/<str:pk>', DeleteCandidateView.as_view(), name='delete_candidate'),
    path('shortlist_candidate/<str:pk>', ShortlistCandidateScreeningView.as_view(), name='shortlist_candidate'),
    path('shortlisted_candidate', ShortlistedCandidatePageView.as_view(), name='shortlisted_candidate'),
    # Account
    path('profile/<str:pk>', ProfilePageView.as_view(), name='profile'),
    path('change_password/<str:pk>', ChangePassword.as_view(), name='change_password'),

]
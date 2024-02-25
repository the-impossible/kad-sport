from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from sport_app.models import *
from sport_app.forms import *
# Create your views here.
class HomePageView(TemplateView):
    template_name = "frontend/index.html"

class LoginPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('app:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(
                        request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('app:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logged out, to continue login again')
        return redirect('app:login')

class RegisterPageView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/register.html"
    success_message = "Registration Successful you can now login"

    def get_success_url(self):
        return reverse("app:login")

class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            total_shortlisted = Screening.objects.filter(status=True).count()
            total_candidate = Screening.objects.all().count()
            total_users = User.objects.all().count()
            total_admin = User.objects.filter(is_staff=True).count()

            context["total_shortlisted"] = total_shortlisted
            context["total_candidate"] = total_candidate
            context["total_users"] = total_users
            context["total_admin"] = total_admin

        else:
            screening = Screening.objects.filter(user=self.request.user)
            if screening:
                context["status"] = screening[0].status
            else:
                context["status"] = None

        return context

class ApplyScreeningPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = ScreeningForm
    template_name = "backend/screening/apply_screening.html"
    success_message = "Your Application is undergoing review"

    def get(self, request, *args, **kwargs):
        if self.request.user.picture.url != "/media/img/user.png":
            has_applied = Screening.objects.filter(user=self.request.user).exists()
            if not has_applied:
                return super().get(request, *args, **kwargs)
            else:
                messages.error(request, "You already have an application!")
                return redirect("app:dashboard")
        else:
            messages.warning(request, "Kindly update profile picture before proceeding to apply!")
            return redirect("app:profile", self.request.user.pk)

    def get_success_url(self):
        return reverse("app:dashboard")

    def get_redirect_url(self):
        return reverse("app:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form = super().form_valid(form)

        return form

class ScreeningStatusPageView(LoginRequiredMixin, TemplateView):
    template_name = "backend/screening/screening_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screening = Screening.objects.filter(user=self.request.user)
        if screening:
            context["status"] = screening[0].status
        else:
            context["status"] = None
        return context

class CreateAdminPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = AdminCreationForm
    template_name = "backend/admin/create_update_admin.html"
    success_message = "Admin account created successfully! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("app:create_admin")

    def form_valid(self, form):
        form.instance.is_staff = True
        form = super().form_valid(form)

        return form

class ManageAdminPageView(LoginRequiredMixin, ListView):
    template_name = "backend/admin/manage_admin.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=True).order_by('-date_joined')

class EditAdminView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/admin/create_update_admin.html"
    form_class = UpdateAdminForm
    success_message = 'Admin Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("app:manage_admin")

class DeleteAdminView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_message = 'Admin Account Deleted Successfully!'
    success_url = reverse_lazy('app:manage_admin')

class ApplyCandidateForScreeningPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Screening
    form_class = ApplyCandidateForm
    template_name = "backend/admin/create_candidate.html"
    success_message = "Candidate has been created and application successful! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("app:apply_candidate")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password = make_password(form.cleaned_data.get('password'))
        name = form.cleaned_data.get('name')
        user = User.objects.create(email=email, phone=phone, password=password, name=name)
        form.instance.user = user
        form = super().form_valid(form)

        return form

class ManageCandidateScreeningPageView(LoginRequiredMixin, ListView):
    template_name = "backend/admin/manage_candidate.html"

    def get_queryset(self):
        return Screening.objects.all().order_by('-date_applied')

class EditCandidateScreeningView(SuccessMessageMixin, LoginRequiredMixin, View):
    model = Screening
    template_name = "backend/admin/update_candidate.html"
    form_class = ApplyCandidateForm
    success_message = 'Candidate Application Updated Successfully!'

    def get(self, request, *args, **kwargs):
        try:
            screening = Screening.objects.get(user=self.kwargs['pk'])
            user = User.objects.get(pk=self.kwargs['pk'])
        except Screening.DoesNotExist:
            messages.error(request, "Unable to get candidate information!")
            return HttpResponseRedirect(reverse("app:manage_candidate"))

        # Initialize forms with instance data
        form1 = ScreeningForm(instance=screening)
        form2 = CandidateUpdateForm(instance=user)

        context = {
            'form1': form1,
            'form2': form2,
            'object': screening,
            'user': user,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Retrieve the Screening object
        try:
            screening = Screening.objects.get(user=self.kwargs['pk'])
            user = User.objects.get(pk=self.kwargs['pk'])
        except Screening.DoesNotExist:
            messages.error(request, "Unable to get candidate information!")
            return HttpResponseRedirect(reverse("app:manage_candidate"))

        # Process the submitted forms
        form1 = ScreeningForm(request.POST,instance=screening)
        form2 = CandidateUpdateForm(request.POST, request.FILES, instance=user)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse("app:manage_candidate"))
        else:
            messages.error(request, "Form submission failed. Please check the data.")
            context = {
                'form1': form1,
                'form2': form2,
                'object': screening,
                'user': user,
            }
            return render(request, self.template_name, context)

class DeleteCandidateView(DeleteAdminView):
    success_message = 'Candidate Account Deleted Successfully!'
    success_url = reverse_lazy('app:manage_candidate')

class ShortlistCandidateScreeningView(SuccessMessageMixin, LoginRequiredMixin, View):
    model = Screening
    template_name = "backend/admin/update_candidate.html"
    form_class = ApplyCandidateForm
    success_message = 'Candidate Shortlisted Successfully!'


    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs['pk'])
            screening = Screening.objects.get(user=user)
            screening.status = True
            messages.success(request, self.success_message)
            screening.save()
        except Screening.DoesNotExist:
            messages.error(request, "Unable to get candidate information!")
        except User.DoesNotExist:
            messages.error(request, "Unable to get candidate information!")
        return HttpResponseRedirect(reverse("app:manage_candidate"))

class ShortlistedCandidatePageView(LoginRequiredMixin, ListView):
    template_name = "backend/admin/shortlisted_candidate.html"

    def get_queryset(self):
        return Screening.objects.filter(status=True).order_by('-date_applied')

class ProfilePageView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "backend/profile.html"
    model = User
    form_class = CandidateUpdateForm
    success_message = 'Account Updated Successfully!'

class ChangePassword(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        password0 = request.POST.get('password0')
        password = request.POST.get('password1')
        password1 = request.POST.get('password2')

        if (password != password1):
            messages.error(request, 'Password does not match!')
            return redirect('app:profile', self.kwargs['pk'])

        if (len(password1) < 6):
            messages.error(request, 'Password too short!')
            return redirect('app:profile', self.kwargs['pk'])

        user = User.objects.get(pk=self.kwargs['pk'])

        if not user.check_password(password0):
            messages.error(request, 'Old password incorrect!')
            return redirect('app:profile', self.kwargs['pk'])

        user.set_password(password)
        user.save()

        messages.success(request, 'Password reset successful!!')
        return redirect('app:login')



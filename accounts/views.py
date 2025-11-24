from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Account created successfully! Please log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please fix the errors.")
        return super().form_invalid(form)


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, self.template_name)


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("login")

from django.shortcuts import render, redirect
from .forms import RegisterForm, ConfirmPasswordForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
    return render(request, 'main/home.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def log_out(request):
    logout(request)
    return redirect('/login')
    # return redirect('/home')


def about(request):
    return render(request, 'about.html')


class DeleteAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'delete_account.html'

    def post(self, request, *args, **kwargs):
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user:
                user.delete()
                messages.success(request, "Your account has been deleted successfully.")
                return redirect('home')
            else:
                messages.error(request, "Incorrect password. Please try again.")
        else:
            messages.error(request, "Please confirm your password.")
        return render(request, self.template_name, {'form': form})


# TODO: if a user clicks on "Forgot password" on the login page, and the provided email is not in the database,
#  the user should be warned that there is no account with that email address.

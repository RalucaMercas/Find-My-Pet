from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from .forms import RegisterForm, ConfirmPasswordForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic.edit import UpdateView

from .models import User, LostPost, FoundPost, PetImage
from .forms import EditProfileForm, LostPostForm, FoundPostForm
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render


def home(request):
    post_type = request.GET.get('post_type', 'lost')  # Default to 'lost'

    if post_type == 'lost':
        posts = LostPost.objects.filter(is_archived=False).prefetch_related('images').order_by('-created_at')
    elif post_type == 'found':
        posts = FoundPost.objects.filter(is_archived=False).prefetch_related('images').order_by('-created_at')
    else:
        posts = []

    return render(request, 'main/home.html', {
        'posts': posts,
        'post_type': post_type,
    })


@login_required(login_url='/login')
def create_post(request, post_type):
    form_class = LostPostForm if post_type == 'lost' else FoundPostForm

    if request.method == 'POST':
        form = form_class(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            images = request.FILES.getlist('images')
            for image in images:
                PetImage.objects.create(
                    content_type=ContentType.objects.get_for_model(post.__class__),
                    object_id=post.id,
                    image=image
                )

            return redirect('/home')
    else:
        form = form_class(user=request.user)

    return render(request, 'main/create_post.html', {'form': form, 'post_type': post_type.capitalize()})


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

    def get(self, request, *args, **kwargs):
        form = ConfirmPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user:
                user.delete()
                return redirect('home')
            else:
                messages.error(request, "Incorrect password. Please try again.")
        else:
            messages.error(request, "Please confirm your password.")
        return render(request, self.template_name, {'form': form})


# TODO: if a user clicks on "Forgot password" on the login page, and the provided email is not in the database,
#  the user should be warned that there is no account with that email address.


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

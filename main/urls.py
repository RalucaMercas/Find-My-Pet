from django.urls import path
from .views import home, sign_up, log_out

urlpatterns = [
    path('', home, name='home'),
    path('home', home, name='home'),
    path('sign-up', sign_up, name='sign_up'),
    path('log-out', log_out, name='log_out'),
]
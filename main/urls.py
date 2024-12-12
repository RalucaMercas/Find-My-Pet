from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home, sign_up, log_out, about, DeleteAccountView, EditProfileView, create_post, my_posts, post_detail, edit_post, delete_post, archive_post, my_archive, unarchive_post
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('home', home, name='home'),
    path('sign-up', sign_up, name='sign_up'),
    path('log-out', log_out, name='log_out'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='admin/password_change_form.html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='admin/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='admin/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='admin/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='admin/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='admin/password_reset_complete.html'),
         name='password_reset_complete'),
    path('about/', about, name='about'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('create_post/<str:post_type>/', create_post, name='create_post'),
    path('my_posts/', my_posts, name='my_posts'),
    path('my_archive/', my_archive, name='my_archive'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('post/<int:post_id>/archive/', archive_post, name='archive_post'),
    path('post/<int:post_id>/unarchive/', unarchive_post, name='unarchive_post'),

]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base, name='base'),
    path('about/', about, name='about'),
    
    path('signup/', signup_view, name='signup'),
    path("logout/", logout_view, name="logout"),
    
    path('login/', login_view, name='login'),
    
    path('profile/', login_required(profile_view), name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html', success_url='/dashboard/'), name='change_password'),

    # Reset password
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    

    path('dashboard/', dashboard, name='dashboard'),
    path('messages/', user_list_view, name='user_list'),
    path('messages/<int:user_id>/', chat_view_by_id, name='chat'),
    
    path('feedback/', feedback_view, name='feedback'),
    path('feedbacks/', view_feedbacks, name='view_feedbacks'),
    path("contact/", contact, name="contact"),

    # prediction # mainApplicationFunctionality20240625

    path('vision-mission/', vision_mission, name='vision_mission'),
    path('gallery/', gallery, name='gallery'),
    path('values-objectives/',values_objectives, name='values_objectives'),
    path('college-emblem/', college_emblem, name='college_emblem'),
    path('principal-message/', principal_message, name='principal_message'),
    path('administrator-message/',administrator_message, name='administrator_message'),
    path('Our_society_and_institution/',Our_society_and_institution, name='our_society_and_institution'),
    path('feedback/', Feedback, name='feedback'),
    path('view-feedback/',view_feedbacks, name='view_feedback'),
    path('admin-messages/',view_messages, name='admin_messages'),
    path('user-messages/', view_messages, name='user_messages'),
    path('delete-message/<int:id>/', delete_message, name='delete_message'),
    path('delete-selected-messages/', delete_selected_messages, name='delete_selected_messages'),
    path('delete-feedback/<int:id>/',delete_feedback, name='delete_feedback'),
    path('delete-selected-feedbacks/',delete_selected_feedbacks, name='delete_selected_feedbacks'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ================================================================
#  CLE BCA College — urls.py
#  Fixes:
#    • Removed duplicate path('feedback/', Feedback, ...) — Feedback
#      is a MODEL not a view, this caused a TypeError crash
#    • Removed duplicate 'view_feedback' / 'admin_messages' names
#    • Fixed redirect target for contact (was '/#contact', now '/')
#    • Kept all real view functions, removed phantom ones
# ================================================================

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    # Auth
    signup_view, login_view, logout_view,
    # Profile
    profile_view, edit_profile,
    # Pages
    base, about, dashboard, gallery,
    vision_mission, values_objectives,
    college_emblem, principal_message,
    administrator_message, Our_society_and_institution,
    # Chat
    user_list_view, chat_view_by_id,
    # Feedback
    feedback_view, view_feedbacks,
    delete_feedback, delete_selected_feedbacks,
    # Contact / Messages
    contact, view_messages,
    delete_message, delete_selected_messages,
)

urlpatterns = [

    # ── Base ────────────────────────────────────────────────────
    path('', base, name='base'),

    # ── Auth ────────────────────────────────────────────────────
    path('signup/',  signup_view,  name='signup'),
    path('login/',   login_view,   name='login'),
    path('logout/',  logout_view,  name='logout'),

    # ── Password change ─────────────────────────────────────────
    path('password/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/change_password.html',
             success_url='/profile/'
         ),
         name='change_password'),

    # ── Password reset ──────────────────────────────────────────
    path('reset-password/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset'),
    path('reset-password/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # ── Profile ─────────────────────────────────────────────────
    path('profile/',      profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # ── Main pages ──────────────────────────────────────────────
    path('about/',     about,     name='about'),
    path('dashboard/', dashboard, name='dashboard'),
    path('gallery/',   gallery,   name='gallery'),

    # ── About sub-pages ─────────────────────────────────────────
    path('vision-mission/',           vision_mission,              name='vision_mission'),
    path('values-objectives/',        values_objectives,           name='values_objectives'),
    path('college-emblem/',           college_emblem,              name='college_emblem'),
    path('principal-message/',        principal_message,           name='principal_message'),
    path('administrator-message/',    administrator_message,       name='administrator_message'),
    path('our-society-institution/',  Our_society_and_institution, name='our_society_and_institution'),

    # ── Chat ────────────────────────────────────────────────────
    path('messages/',            user_list_view,   name='user_list'),
    path('messages/<int:user_id>/', chat_view_by_id, name='chat'),

    # ── Feedback ────────────────────────────────────────────────
    path('feedback/',                    feedback_view,              name='feedback'),
    path('view-feedback/',               view_feedbacks,             name='view_feedback'),
    path('delete-feedback/<int:id>/',    delete_feedback,            name='delete_feedback'),
    path('delete-selected-feedbacks/',   delete_selected_feedbacks,  name='delete_selected_feedbacks'),

    # ── Contact / Admin messages ─────────────────────────────────
    path('contact/',                     contact,                   name='contact'),
    path('admin-messages/',              view_messages,             name='admin_messages'),
    path('user-messages/',               view_messages,             name='user_messages'),
    path('delete-message/<int:id>/',     delete_message,            name='delete_message'),
    path('delete-selected-messages/',    delete_selected_messages,  name='delete_selected_messages'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
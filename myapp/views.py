# ================================================================
#  CLE BCA College — views.py
#  Fixes: duplicate URL names, wrong redirect, Feedback import clash
# ================================================================

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm, FeedbackForm, ProfileForm
from .models import ContactMessages, Feedback, Message

logger = logging.getLogger(__name__)
User   = get_user_model()


# ================================================================
#  HELPERS
# ================================================================

def _send_email_safe(subject, body, recipient_list):
    """Send email without crashing the request if it fails."""
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    if not recipient_list or not from_email:
        return
    try:
        send_mail(subject, body, from_email, recipient_list, fail_silently=False)
    except Exception as exc:
        logger.exception("Email send failed: %s", exc)


# ================================================================
#  BASE
# ================================================================

def base(request):
    return render(request, 'base.html')


# ================================================================
#  AUTHENTICATION
# ================================================================

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.name}! Your account has been created.")
            return redirect('dashboard')
        # Show individual field errors as toast messages
        for field, errs in form.errors.items():
            for err in errs:
                label = form.fields[field].label or field if field != '__all__' else ''
                messages.error(request, f"{label}: {err}" if label else err)
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email    = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'registration/login.html')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ================================================================
#  PROFILE
# ================================================================

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'account/edit_profile.html', {'form': form})


# ================================================================
#  DASHBOARD
# ================================================================

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


# ================================================================
#  STATIC / ABOUT PAGES
# ================================================================

def about(request):
    return render(request, 'about/about.html')

def vision_mission(request):
    return render(request, 'vision_mission.html')

def values_objectives(request):
    return render(request, 'values_objectives.html')

def college_emblem(request):
    return render(request, 'college_emblem.html')

def principal_message(request):
    return render(request, 'principal_message.html')

def administrator_message(request):
    return render(request, 'administrator_message.html')

def Our_society_and_institution(request):
    return render(request, 'our_society_and_institution.html')

def gallery(request):
    return render(request, 'gallery.html')


# ================================================================
#  CHAT
# ================================================================

@login_required
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id).order_by('name')
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def chat_view_by_id(request, user_id):
    other_user    = get_object_or_404(User, id=user_id)
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user,   receiver=request.user)
    ).order_by('timestamp').select_related('sender', 'receiver')

    if request.method == 'POST':
        text  = request.POST.get('text', '').strip()
        image = request.FILES.get('image')
        if text or image:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text,
                image=image
            )
        return redirect('chat', user_id=other_user.id)

    return render(request, 'users/chat.html', {
        'messages':  messages_list,
        'receiver':  other_user,
    })


# ================================================================
#  FEEDBACK
# ================================================================

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb      = form.save(commit=False)
            fb.user = request.user
            fb.save()

            # Email admins
            admin_emails = [addr for _, addr in getattr(settings, 'ADMINS', [])]
            if not admin_emails:
                fallback = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                if fallback:
                    admin_emails = [fallback]

            _send_email_safe(
                subject=f"New Feedback from {request.user.name}",
                body=(
                    f"User:  {request.user.name}\n"
                    f"Email: {request.user.email}\n\n"
                    f"--- Message ---\n{form.cleaned_data.get('message', '')}"
                ),
                recipient_list=admin_emails,
            )

            messages.success(request, "Thank you for your feedback!")
            return render(request, 'feedback/feedback_thanks.html')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form})


@login_required
def view_feedbacks(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('dashboard')

    feedbacks = Feedback.objects.all().select_related('user').order_by('-created_at')
    return render(request, 'feedback/view_feedbacks.html', {'feedbacks': feedbacks})


@login_required
def delete_feedback(request, id):
    if not request.user.is_superuser:
        return redirect('dashboard')
    fb = get_object_or_404(Feedback, id=id)
    fb.delete()
    messages.success(request, "Feedback deleted.")
    return redirect('view_feedback')


@login_required
def delete_selected_feedbacks(request):
    if request.method == 'POST' and request.user.is_superuser:
        ids = request.POST.getlist('selected_feedbacks')
        deleted, _ = Feedback.objects.filter(id__in=ids).delete()
        messages.success(request, f"{deleted} feedback(s) deleted.")
    return redirect('view_feedback')


# ================================================================
#  CONTACT
# ================================================================

@login_required
def contact(request):
    # Staff / superusers should not see the contact form
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            ContactMessages.objects.create(name=name, email=email, message=message_text)
            messages.success(request, "Message sent successfully!")
        else:
            messages.error(request, "Please fill in all fields.")

    return redirect('/')


@staff_member_required
def view_messages(request):
    msgs = ContactMessages.objects.all().order_by('-created_at')
    return render(request, 'user_messages.html', {'messages': msgs})


@staff_member_required
def delete_message(request, id):
    msg = get_object_or_404(ContactMessages, id=id)
    msg.delete()
    messages.success(request, "Message deleted.")
    return redirect('user_messages')


@staff_member_required
def delete_selected_messages(request):
    if request.method == 'POST':
        ids     = request.POST.getlist('selected_messages')
        deleted, _ = ContactMessages.objects.filter(id__in=ids).delete()
        messages.success(request, f"{deleted} message(s) deleted.")
    return redirect('user_messages')


# ================================================================
#  CHATBOT INTERACTION (standalone page if needed)
# ================================================================

@login_required
def interaction(request):
    return render(request, 'interaction/chatbot.html')
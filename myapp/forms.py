# ================================================================
#  CLE BCA College — forms.py
# ================================================================

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Feedback

CustomUser = get_user_model()

# Shared widget style helper
def _ctrl(placeholder='', input_type='text', extra=''):
    return {'class': f'form-control {extra}', 'placeholder': placeholder}


# ================================================================
#  SIGNUP FORM
# ================================================================
class CustomUserCreationForm(UserCreationForm):

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs=_ctrl('Full Name'))
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs=_ctrl('Email Address'))
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs=_ctrl('Create a password'))
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs=_ctrl('Confirm your password'))
    )

    class Meta:
        model  = CustomUser
        fields = ('name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user          = super().save(commit=False)
        user.email    = self.cleaned_data['email']
        user.name     = self.cleaned_data['name']
        user.username = self.cleaned_data['email']   # keep username = email
        if commit:
            user.save()
        return user


# ================================================================
#  PROFILE FORM
# ================================================================
class ProfileForm(forms.ModelForm):

    class Meta:
        model  = CustomUser
        fields = ['name', 'email', 'contact', 'age', 'gender']
        widgets = {
            'name':    forms.TextInput(attrs=_ctrl('Full Name')),
            'email':   forms.EmailInput(attrs={**_ctrl('Email'), 'readonly': 'readonly'}),
            'contact': forms.TextInput(attrs=_ctrl('Phone / WhatsApp')),
            'age':     forms.NumberInput(attrs=_ctrl('Age')),
            'gender':  forms.Select(attrs={'class': 'form-select'}),
        }


# ================================================================
#  FEEDBACK FORM
# ================================================================
class FeedbackForm(forms.ModelForm):

    class Meta:
        model  = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows':        4,
                'placeholder': 'Write your feedback here…',
                'class':       'form-control shadow-sm rounded-3',
                'style':       'resize:none;',
            }),
        }
        labels = {'message': ''}
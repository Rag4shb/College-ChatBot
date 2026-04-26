# ================================================================
#  CLE BCA College — models.py
# ================================================================

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone


# ================================================================
#  CUSTOM USER MANAGER
# ================================================================
class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # Auto-set username to email so Django admin works
        extra_fields.setdefault('username', email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, name, password, **extra_fields)


# ================================================================
#  CUSTOM USER MODEL
# ================================================================
class CustomUser(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [
        ('male',   'Male'),
        ('female', 'Female'),
        ('other',  'Other'),
    ]

    # Core fields
    email    = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    name     = models.CharField(max_length=100)

    # Extra profile fields
    contact = models.CharField(max_length=15, blank=True, null=True)
    age     = models.PositiveIntegerField(null=True, blank=True)
    gender  = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    # Flags
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_admin     = models.BooleanField(default=False)
    date_joined  = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        verbose_name        = 'User'
        verbose_name_plural = 'Users'
        ordering            = ['email']

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def save(self, *args, **kwargs):
        # Keep username in sync with email automatically
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    # PermissionsMixin already provides has_perm / has_module_perms
    # but we keep is_admin check consistent
    def has_perm(self, perm, obj=None):
        return self.is_active and (self.is_admin or self.is_superuser)

    def has_module_perms(self, app_label):
        return self.is_active and (self.is_admin or self.is_superuser)


# ================================================================
#  MESSAGE MODEL
# ================================================================
class Message(models.Model):
    sender   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True, blank=True
    )
    text              = models.TextField(blank=True)
    image             = models.ImageField(upload_to='messages/', blank=True, null=True)
    timestamp         = models.DateTimeField(auto_now_add=True)
    is_group_message  = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        to = self.receiver.name if self.receiver else 'Group'
        return f"{self.sender.name} → {to}"


# ================================================================
#  FEEDBACK MODEL
# ================================================================
class Feedback(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved   = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        ts = self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else 'N/A'
        return f"Feedback from {self.user.name} at {ts}"


# ================================================================
#  CONTACT MESSAGES MODEL
# ================================================================
class ContactMessages(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
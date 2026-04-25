# ================================================================
#  CLE BCA College — admin.py
# ================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.timezone import localtime
from .models import *

# ================================================================
#  BRANDING
# ================================================================
admin.site.site_header  = "CLE BCA College — Administrator"
admin.site.site_title   = "CLE BCA Admin Panel"
admin.site.index_title  = "Welcome to the Admin Dashboard"


# ================================================================
#  CUSTOM USER
# ================================================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display  = ('avatar_badge', 'email', 'name', 'contact', 'gender', 'role_badge', 'is_active')
    list_filter   = ('is_staff', 'is_superuser', 'is_active', 'gender')
    search_fields = ('email', 'name', 'contact')
    ordering      = ('email',)

    fieldsets = (
        ('Account',         {'fields': ('username', 'email', 'password')}),
        ('Personal Info',   {'fields': ('name', 'contact', 'age', 'gender')}),
        ('Permissions',     {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')

    @admin.display(description='User')
    def avatar_badge(self, obj):
        initials = (obj.name or obj.email)[0].upper()
        return format_html(
            '<span style="'
            'display:inline-flex;align-items:center;justify-content:center;'
            'width:30px;height:30px;border-radius:50%;'
            'background:#1a56db;color:#fff;font-weight:700;font-size:13px;">'
            '{}</span>',
            initials
        )

    @admin.display(description='Role')
    def role_badge(self, obj):
        if obj.is_superuser:
            color, label = '#7c3aed', 'Superuser'
        elif obj.is_staff:
            color, label = '#1a56db', 'Staff'
        else:
            color, label = '#059669', 'Student'
        return format_html(
            '<span style="'
            'background:{};color:#fff;padding:2px 10px;'
            'border-radius:999px;font-size:11px;font-weight:600;">'
            '{}</span>',
            color, label
        )


# ================================================================
#  FEEDBACK
# ================================================================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display  = ('user', 'short_message', 'status_badge', 'created_at')
    list_filter   = ('resolved',)
    search_fields = ('user__name', 'user__email', 'message')
    readonly_fields = ('user', 'message', 'created_at')
    actions       = ['mark_resolved', 'mark_unresolved']

    @admin.display(description='Message')
    def short_message(self, obj):
        msg = obj.message or ''
        return msg[:60] + ('…' if len(msg) > 60 else '')

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.resolved:
            return format_html(
                '<span style="background:#059669;color:#fff;padding:2px 10px;'
                'border-radius:999px;font-size:11px;font-weight:600;">✔ Resolved</span>'
            )
        return format_html(
            '<span style="background:#dc2626;color:#fff;padding:2px 10px;'
            'border-radius:999px;font-size:11px;font-weight:600;">⏳ Pending</span>'
        )

    @admin.action(description='Mark selected as Resolved')
    def mark_resolved(self, request, queryset):
        updated = queryset.update(resolved=True)
        self.message_user(request, f'{updated} feedback(s) marked as resolved.')

    @admin.action(description='Mark selected as Unresolved')
    def mark_unresolved(self, request, queryset):
        updated = queryset.update(resolved=False)
        self.message_user(request, f'{updated} feedback(s) marked as unresolved.')


# ================================================================
#  MESSAGES
# ================================================================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display    = ('id', 'sender', 'receiver', 'short_text', 'type_badge', 'formatted_time')
    search_fields   = ('sender__email', 'sender__name', 'receiver__email', 'text')
    list_filter     = ('is_group_message', 'timestamp')
    readonly_fields = ('timestamp',)
    ordering        = ('-timestamp',)
    date_hierarchy  = 'timestamp'

    @admin.display(description='Message')
    def short_text(self, obj):
        text = obj.text or ''
        return text[:50] + ('…' if len(text) > 50 else '')

    @admin.display(description='Type')
    def type_badge(self, obj):
        if obj.is_group_message:
            return format_html(
                '<span style="background:#f59e0b;color:#000;padding:2px 10px;'
                'border-radius:999px;font-size:11px;font-weight:600;">Group</span>'
            )
        return format_html(
            '<span style="background:#6b7280;color:#fff;padding:2px 10px;'
            'border-radius:999px;font-size:11px;font-weight:600;">Direct</span>'
        )

    @admin.display(description='Time')
    def formatted_time(self, obj):
        return localtime(obj.timestamp).strftime('%d %b %Y, %I:%M %p')


# ================================================================
#  CONTACT MESSAGES
# ================================================================
@admin.register(ContactMessages)
class ContactMessagesAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email_link', 'short_message', 'created_at')
    search_fields   = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    ordering        = ('-created_at',)
    date_hierarchy  = 'created_at'

    @admin.display(description='Email')
    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    @admin.display(description='Message')
    def short_message(self, obj):
        msg = obj.message or ''
        return msg[:70] + ('…' if len(msg) > 70 else '')
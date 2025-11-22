from .models import UserSession, UserInteraction
from django.contrib import admin


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['session_id']


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['session', 'product', 'interaction_type', 'timestamp']
    list_filter = ['interaction_type', 'timestamp']
    readonly_fields = ['timestamp']
    search_fields = ['session__session_id', 'product__name']
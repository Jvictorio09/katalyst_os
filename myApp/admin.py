from django.contrib import admin
from .models import Tool, Project, Activity

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "owner", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "owner", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    readonly_fields = ("created_at",)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("text", "kind", "user", "created_at")
    list_filter = ("kind",)
    search_fields = ("text",)
    readonly_fields = ("created_at",)

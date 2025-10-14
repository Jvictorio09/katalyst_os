# myProject/urls.py
from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    # HTMX endpoints
    path('tools/<slug:slug>/toggle/', views.toggle_tool, name='tool_toggle'),
    path('activity/more/', views.activity_more, name='activity_more'),

    # NEW: AI generation (must come BEFORE the detail route)
    path('tools/<slug:slug>/generate/', views.tool_generate, name='tool_generate'),

    # Tool detail pages
    path('tools/<slug:slug>/', views.tool_detail, name='tool_detail'),
]

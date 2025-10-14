from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Tool, Project, Activity
from .forms import ContentRequestForm

# OpenAI (new SDK)
from django.conf import settings
from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    tools = Tool.objects.filter(owner=request.user).order_by("-created_at")[:12]
    counts = {
        "active_tools": Tool.objects.filter(owner=request.user, is_active=True).count(),
        "projects": Project.objects.filter(owner=request.user).count(),
        "team_members": 24,
    }
    activity = Activity.objects.filter(user=request.user).order_by("-created_at")[:10]
    return render(request, 'dashboard.html', {
        'tools': tools,
        'counts': counts,
        'activity': activity,
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def toggle_tool(request, slug):
    tool = get_object_or_404(Tool, slug=slug, owner=request.user)
    tool.is_active = not tool.is_active
    tool.save()
    return render(request, '_tool_badge.html', {'tool': tool})

@login_required
def activity_more(request):
    offset = int(request.GET.get('offset', 10))
    more = Activity.objects.filter(user=request.user).order_by("-created_at")[offset:offset+10]
    return render(request, '_activity_items.html', {'activity': more})

@login_required
def tool_detail(request, slug):
    """Display individual tool page based on slug"""
    tool = get_object_or_404(Tool, slug=slug, owner=request.user)
    
    # Get recent activities for this tool type
    kind_key = tool.icon or "content"
    recent_activities = Activity.objects.filter(
        user=request.user,
        kind=kind_key
    ).order_by('-created_at')[:6]
    
    # Use specific template for each tool
    template_map = {
        'email-copilot': 'tools/email-copilot.html',
        'image-generator': 'tools/image-generator.html',
        'video-generator': 'tools/video-generator.html',
        'code-assistant': 'tools/code-assistant.html',
        'content-writer': 'tools/content-writer.html',
        'analytics': 'tools/analytics.html',
    }
    
    template = template_map.get(slug, 'tools/content-writer.html')  # fallback
    
    return render(request, template, {
        'tool': tool,
        'recent_activities': recent_activities,
    })

@login_required
def tool_generate(request, slug):
    """
    HTMX target: handles AI generation for different tool types
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid method")

    tool = get_object_or_404(Tool, slug=slug, owner=request.user)
    
    # Handle different tool types
    if slug == 'content-writer':
        return handle_content_generation(request, tool)
    elif slug == 'email-copilot':
        return handle_email_generation(request, tool)
    elif slug == 'code-assistant':
        return handle_code_generation(request, tool)
    elif slug == 'image-generator':
        return handle_image_generation(request, tool)
    elif slug == 'video-generator':
        return handle_video_generation(request, tool)
    else:
        return render(request, 'tools/_generated.html', {
            'error': f"Generation not yet implemented for {tool.name}",
            'content': "",
        })

def handle_content_generation(request, tool):
    """Handle content generation specifically"""
    form = ContentRequestForm(request.POST)
    
    if not form.is_valid():
        return render(request, 'tools/_generated.html', {
            'error': "Please fill the required fields.",
            'content': "",
        })

    data = form.cleaned_data
    length_map = {"short": 300, "medium": 700, "long": 1200}
    target_words = length_map.get(data["length"], 500)

    system = (
        "You are Katalyst OS's Content Writer. "
        "Write clear, specific, engaging content tailored to the requested type, tone, and audience. "
        "Use short paragraphs, helpful subheads, and markdown. Avoid fluff."
    )

    user_prompt = f"""
Content Type: {dict(form.fields['content_type'].choices)[data['content_type']]}
Topic: {data['topic']}
Audience: {data.get('audience') or 'General'}
Tone: {dict(form.fields['tone'].choices)[data['tone']]}
Key Points: {data.get('key_points') or 'N/A'}
Target Length (approx): {target_words} words

Instructions:
- Start with a strong hook for the audience.
- Use 2–4 useful subheads.
- Include a concise CTA if relevant.
- Keep it factual, readable, on-brand.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return render(request, 'tools/_generated.html', {
            'error': f"Generation failed: {e}",
            'content': "",
        })

    # Log as content activity
    Activity.objects.create(
        user=request.user,
        kind="content",
        text=f"Generated {data['content_type']} on '{data['topic']}'"
    )

    return render(request, 'tools/_generated.html', {
        'error': "",
        'content': content,
    })

def handle_email_generation(request, tool):
    """Handle email generation specifically"""
    return render(request, 'tools/_generated.html', {
        'error': "",
        'content': "Email generation will be implemented here...",
    })

def handle_code_generation(request, tool):
    """Handle code generation specifically"""
    return render(request, 'tools/_generated.html', {
        'error': "",
        'content': "Code generation will be implemented here...",
    })

def handle_image_generation(request, tool):
    """Handle image generation specifically"""
    return render(request, 'tools/_generated.html', {
        'error': "",
        'content': "Image generation will be implemented here...",
    })

def handle_video_generation(request, tool):
    """Handle video generation specifically"""
    return render(request, 'tools/_generated.html', {
        'error': "",
        'content': "Video generation will be implemented here...",
    })

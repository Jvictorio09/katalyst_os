from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    """Handle user login"""
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
    """Display the dashboard for authenticated users"""
    return render(request, 'dashboard.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')

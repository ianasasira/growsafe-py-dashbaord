from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:overview')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard:overview')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account is suspended.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'tenant':
                return redirect('tenant_dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid email or password'})
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Access denied")
    return render(request, 'core/admin/dashboard.html')

@login_required
def tenant_dashboard(request):
    if request.user.role != 'tenant':
        return HttpResponseForbidden("Access denied")
    return render(request, 'core/tenant/dashboard.html')
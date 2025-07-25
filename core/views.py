from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Building
from .forms import BuildingForm

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
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied: You are not authorized to view this page.")
        return HttpResponseForbidden("Access denied")
    return render(request, 'core/admin_dashboard.html')

@login_required
def tenant_dashboard(request):
    if request.user.role != 'tenant':
        messages.error(request, "Access denied: You are not authorized to view this page.")
        return HttpResponseForbidden("Access denied")
    return render(request, 'core/tenant_dashboard.html')

class BuildingListView(ListView):
    model = Building
    template_name = 'core/building_list.html'
    context_object_name = 'buildings'

    def get(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, "Access denied: You are not authorized to view this page.")
            return HttpResponseForbidden("Access denied")
        return super().get(request, *args, **kwargs)

class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'core/building_form.html'
    success_url = reverse_lazy('building_list')

    def get(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, "Access denied: You are not authorized to view this page.")
            return HttpResponseForbidden("Access denied")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Building '{form.instance.name}' created successfully.")
        return response

class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'core/building_form.html'
    success_url = reverse_lazy('building_list')

    def get(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, "Access denied: You are not authorized to view this page.")
            return HttpResponseForbidden("Access denied")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Building '{form.instance.name}' updated successfully.")
        return response

class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'core/building_confirm_delete.html'
    success_url = reverse_lazy('building_list')

    def get(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, "Access denied: You are not authorized to view this page.")
            return HttpResponseForbidden("Access denied")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, f"Building '{name}' deleted successfully.")
        return response
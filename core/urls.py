from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('buildings/', views.BuildingListView.as_view(), name='building_list'),
    path('buildings/add/', views.BuildingCreateView.as_view(), name='building_create'),
    path('buildings/<int:pk>/edit/', views.BuildingUpdateView.as_view(), name='building_update'),
    path('buildings/<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='building_delete'),
    path('units/', views.UnitListView.as_view(), name='unit_list'),
    path('units/add/', views.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),
    path('tenants/', views.TenantListView.as_view(), name='tenant_list'),
    path('tenants/add/', views.TenantCreateView.as_view(), name='tenant_create'),
    path('tenants/<int:pk>/edit/', views.TenantUpdateView.as_view(), name='tenant_update'),
    path('tenants/<int:pk>/delete/', views.TenantDeleteView.as_view(), name='tenant_delete'),
    path('tenants/<int:pk>/assign/', views.TenantAssignView.as_view(), name='tenant_assign'),
    path('payments/', views.RentPaymentListView.as_view(), name='rent_payment_list'),
    path('payments/add/', views.RentPaymentCreateView.as_view(), name='rent_payment_create'),
    path('payments/<int:pk>/edit/', views.RentPaymentUpdateView.as_view(), name='rent_payment_update'),
    path('payments/<int:pk>/delete/', views.RentPaymentDeleteView.as_view(), name='rent_payment_delete'),
]
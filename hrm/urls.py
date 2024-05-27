from django.urls import path
from .views import CustomLoginView, register, admin_dashboard, dashboard, leave_request, approve_leave, reject_leave, home, company_detail, branch_detail, custom_logout_view, delete_company, delete_branch, delete_employee

urlpatterns = [
    path('', home, name='home'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('company/<int:company_id>/', company_detail, name='company_detail'),
    path('branch/<int:branch_id>/', branch_detail, name='branch_detail'),
    path('register/<slug:company_slug>/', register, name='register'),
    path('login/<slug:company_slug>/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('leave-request/', leave_request, name='leave_request'),
    path('approve-leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('reject-leave/<int:leave_id>/', reject_leave, name='reject_leave'),
    path('delete-company/<int:company_id>/', delete_company, name='delete_company'),
    path('delete-branch/<int:branch_id>/', delete_branch, name='delete_branch'),
    path('delete-employee/<int:employee_id>/', delete_employee, name='delete_employee'),
]

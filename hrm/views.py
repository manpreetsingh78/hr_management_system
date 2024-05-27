from django.shortcuts import render, redirect, get_object_or_404,resolve_url
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .forms import CustomUserCreationForm, LeaveRequestForm, CompanyForm, HRCreationForm, StaffCreationForm,BranchForm
from django.views import View
from django.contrib.auth import logout
from .models import LeaveRequest, Employee, Branch, Company

@login_required
def custom_logout_view(request):
    if request.user.is_authenticated:
        try:
            company_slug = request.user.employee.branch.company.slug
            logout(request)
            return redirect(reverse('login/', kwargs={'company_slug': company_slug}))
        except AttributeError:
            logout(request)
            return redirect(reverse('home/'))
    logout(request)
    return redirect(reverse('home/'))

def home(request):
    companies = Company.objects.all()
    if not companies.exists():
        return redirect('admin/')
    return render(request, 'home.html', {'companies': companies})

@user_passes_test(lambda u: u.is_superuser)
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    messages.success(request, 'Company deleted successfully.')
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    company_id = branch.company.id
    branch.delete()
    messages.success(request, 'Branch deleted successfully.')
    return redirect('company_detail', company_id=company_id)

@user_passes_test(lambda u: u.is_superuser)
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    branch_id = employee.branch.id
    employee.user.delete()  # This will also delete the Employee instance
    messages.success(request, 'Employee deleted successfully.')
    return redirect('branch_detail', branch_id=branch_id)

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    companies = Company.objects.all()
    company_form = CompanyForm()

    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_form.save()
            messages.success(request, 'Company created successfully.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Error creating company. Please check the form and try again.')


    return render(request, 'admin_dashboard.html', {
        'companies': companies,
        'company_form': company_form,
    })

@user_passes_test(lambda u: u.is_superuser)
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    branches = Branch.objects.filter(company=company)
    company_form = CompanyForm()
    branch_form = BranchForm(initial={'company': company})
    
    if request.method == 'POST':
        branch_form = BranchForm(request.POST)
        if branch_form.is_valid():
            branch_form.save()
            messages.success(request, 'Branch created successfully.')
            return redirect('company_detail', company_id=company.id)
        else:
            messages.error(request, 'Error creating branch. Please check the form and try again.')

    
    return render(request, 'company_detail.html', {
        'company': company, 
        'branches': branches, 
        'company_form': company_form, 
        'branch_form': branch_form,
    })

@user_passes_test(lambda u: u.is_superuser)
def branch_detail(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    employees = Employee.objects.filter(branch=branch)
    hr_form = HRCreationForm(initial={'branch': branch})
    staff_form = StaffCreationForm(initial={'branch': branch})
    
    if request.method == 'POST':
        if 'create_hr' in request.POST:
            hr_form = HRCreationForm(request.POST)
            if hr_form.is_valid():
                hr_form.save()
                messages.success(request, 'HR created successfully.')
                return redirect('branch_detail', branch_id=branch.id)
            else:
                messages.error(request, 'Error creating HR. Please check the form and try again.')
   
        elif 'create_staff' in request.POST:
            staff_form = StaffCreationForm(request.POST)
            if staff_form.is_valid():
                staff_form.save()
                messages.success(request, 'Staff created successfully.')
                return redirect('branch_detail', branch_id=branch.id)
            else:
                messages.error(request, 'Error creating staff. Please check the form and try again.')

    
    return render(request, 'branch_detail.html', {
        'branch': branch, 
        'employees': employees, 
        'hr_form': hr_form, 
        'staff_form': staff_form,
    })


def register(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            branch = form.cleaned_data.get('branch')
            Employee.objects.create(user=user, branch=branch, position='Staff')
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error during registration. Please check the form and try again.')
    else:
        form = CustomUserCreationForm()
        form.fields['branch'].queryset = Branch.objects.filter(company=company)
    return render(request, 'registration/register.html', {'form': form, 'company': company})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_slug = self.kwargs.get('company_slug')
        context['company'] = get_object_or_404(Company, slug=company_slug)
        return context
    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please check your username and password and try again.')
        return super().form_invalid(form)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')
@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
        # return render(request, 'admin_dashboard.html')
    elif request.user.is_hr:
        employee = Employee.objects.get(user=request.user)
        branch = employee.branch
        leave_requests = LeaveRequest.objects.filter(employee__branch=branch)
        return render(request, 'hr_dashboard.html', {'leave_requests': leave_requests})
    else:
        leave_requests = LeaveRequest.objects.filter(employee__user=request.user)
        return render(request, 'staff_dashboard.html', {'leave_requests': leave_requests})
@login_required
def leave_request(request):
    print(request.user)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            emp = Employee.objects.get(user=request.user)
            leave.employee = emp
            leave.save()
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error submitting leave request. Please check the form and try again.')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_request.html', {'form': form})
@login_required
def approve_leave(request, leave_id):
    leave_request = LeaveRequest.objects.get(id=leave_id)
    leave_request.approved = True
    leave_request.rejected = False
    leave_request.save()
    messages.success(request, 'Leave request approved successfully.')
    return redirect('dashboard')
@login_required
def reject_leave(request, leave_id):
    leave_request = LeaveRequest.objects.get(id=leave_id)
    leave_request.approved = False
    leave_request.rejected = True
    leave_request.save()
    messages.success(request, 'Leave request rejected successfully.')
    return redirect('dashboard')

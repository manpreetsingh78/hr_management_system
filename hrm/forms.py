from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, LeaveRequest, Branch, Company,Employee

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'company']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company': forms.Select(attrs={'class': 'form-control'}),
        }

class HRCreationForm(UserCreationForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'branch')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_hr = True
        if commit:
            user.save()
            Employee.objects.create(user=user, branch=self.cleaned_data['branch'], position='HR').save()
        return user

class StaffCreationForm(UserCreationForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'branch')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
            Employee.objects.create(user=user, branch=self.cleaned_data['branch'], position='Staff').save()
        return user

class CustomUserCreationForm(UserCreationForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'branch', 'is_hr', 'is_staff')

class LeaveRequestForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
    reason = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3
    }))

    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']

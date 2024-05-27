from django.contrib import admin
from .models import CustomUser, Company, Branch, Employee, LeaveRequest

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Employee)
admin.site.register(LeaveRequest)

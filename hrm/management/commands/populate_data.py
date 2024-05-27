from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
from hrm.models import Company, Branch, Employee

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        companies = []
        branches = []
        users = []
        employees = []

        for _ in range(3):  # 3 companies
            company_name = fake.company()
            company = Company(
                name=company_name,
                address=fake.address(),
                slug=slugify(company_name)
            )
            companies.append(company)

        Company.objects.bulk_create(companies)
        self.stdout.write(self.style.SUCCESS('Companies created'))

        for company in Company.objects.all():
            for _ in range(2):  # 2 branches per company
                branch_name = fake.city()
                branch = Branch(
                    name=branch_name,
                    address=fake.address(),
                    company=company
                )
                branches.append(branch)

        Branch.objects.bulk_create(branches)
        self.stdout.write(self.style.SUCCESS('Branches created'))

        for branch in Branch.objects.all():
            for _ in range(1):  # 1 HR per branch
                username = fake.user_name()
                email = fake.email()
                password = 'password'
                user = User(
                    username=username,
                    email=email,
                    is_hr=True,
                    is_staff=True
                )
                user.set_password(password)
                users.append(user)
                employees.append(Employee(
                    user=user,
                    branch=branch,
                    position='HR'
                ))

            for _ in range(5):  # 5 staff per branch
                username = fake.user_name()
                email = fake.email()
                password = 'password'
                user = User(
                    username=username,
                    email=email,
                    is_staff=True
                )
                user.set_password(password)
                users.append(user)
                employees.append(Employee(
                    user=user,
                    branch=branch,
                    position='Staff'
                ))

        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('Users created'))

        # We need to fetch the newly created users to assign to employees
        for employee in employees:
            employee.user = User.objects.get(username=employee.user.username)

        Employee.objects.bulk_create(employees)
        self.stdout.write(self.style.SUCCESS('Employees created'))

        self.stdout.write(self.style.SUCCESS('Data Created'))

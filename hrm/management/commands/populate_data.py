from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
import random
from hrm.models import Company, Branch, Employee

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(3):  # 5 companies
            company_name = fake.company()
            company = Company.objects.create(
                name=company_name,
                address=fake.address(),
                slug=slugify(company_name)
            )
            # self.stdout.write(self.style.SUCCESS(f'Company "{company.name}" created'))

            for _ in range(5):  # 10 branches per company
                branch_name = fake.city()
                branch = Branch.objects.create(
                    name=branch_name,
                    address=fake.address(),
                    company=company
                )
                # self.stdout.write(self.style.SUCCESS(f'Branch "{branch.name}" created for company "{company.name}"'))

                for _ in range(3):  # 3 HRs per branch
                    username = fake.user_name()
                    email = fake.email()
                    password = 'password'
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        is_hr=True,
                        is_staff=True
                    )
                    Employee.objects.create(
                        user=user,
                        branch=branch,
                        position='HR'
                    )
                    # self.stdout.write(self.style.SUCCESS(f'HR "{user.username}" created for branch "{branch.name}"'))

                for _ in range(10):  # 10 staff per branch
                    username = fake.user_name()
                    email = fake.email()
                    password = 'password'
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        is_staff=True
                    )
                    Employee.objects.create(
                        user=user,
                        branch=branch,
                        position='Staff'
                    )
                    # self.stdout.write(self.style.SUCCESS(f'Staff "{user.username}" created for branch "{branch.name}"'))
        self.stdout.write(self.style.SUCCESS(f'Data Created'))

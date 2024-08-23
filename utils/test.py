from django.contrib.auth import get_user_model
from django.test import TestCase
from departments.models import Department



class SetUpInitial(TestCase):
    """ Provider departaments and user for initial test case"""
    User = get_user_model()
    def setUp(self):
        departments = [
            {"name":"Administração", "description":"Departamento Administrativo"},
            {"name": "TI", "description": "Departamento de Tecnologia da Informação"},
        ]

        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                name=dept_data["name"],
                defaults={"description": dept_data["description"], "owner_id":1},
            )

        self.user = self.User.objects.create_user(email="testuser@123.com", password="password")
        self.user.departments.add(Department.objects.get(id=1))
        self.client.login(email="testuser@123.com", password="password")
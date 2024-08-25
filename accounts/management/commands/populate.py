from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from departments.models import Department


class Command(BaseCommand):
    help = "Populate the Department table and edit user ID 1"

    def handle(self, *args, **kwargs):
        # Crie os departamentos
        departments = [
            {"name": " Administração", "description": "Departamento Administrativo"},
            {"name": "Financeiro", "description": "Departamento Financeiro"},
            {"name": "Recursos Humanos", "description": "Departamento de RH"},
            {"name": "TI", "description": "Departamento de Tecnologia da Informação"},
        ]

        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                name=dept_data["name"],
                defaults={"description": dept_data["description"], "owner_id": 1},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Department "{department.name}" created successfully!'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Department "{department.name}" already exists.')
                )

        # Adicionar departamentos ao usuário de ID 1
        User = get_user_model()
        user = User.objects.get(id=1)
        user.departments.add(*Department.objects.all())
        user.save()

        self.stdout.write(
            self.style.SUCCESS("Departments associated with the user successfully!")
        )

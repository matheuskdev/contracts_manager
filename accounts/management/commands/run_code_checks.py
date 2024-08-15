import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run code checks: flake8, black, and isort."

    def handle(self, *args, **kwargs):
        commands = ["flake8 .", "black .", "isort ."]

        for command in commands:
            self.stdout.write(f"Running {command}...")
            result = subprocess.run(command, shell=True)
            if result.returncode != 0:
                self.stdout.write(self.style.ERROR(f"{command} found issues."))
                exit(result.returncode)

        self.stdout.write(
            self.style.SUCCESS("All checks passed successfully!")
        )

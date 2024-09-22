from django.urls import reverse
from django.utils import timezone
from contracts.models import Contract
from folders.models import Folder
from departments.models import Department
from expirations.models import Expiration
from utils.test import SetUpInitial


class ContractExpirationTests(SetUpInitial):
    def setUp(self):
        """
        Set up objects for each test:
        - Create user, folder, department and contracts with various expiration statuses.
        """
        super().setUp()
        self.set_permission(Expiration, "view_expiration")

        self.folder = Folder.objects.create(name="Folder1", owner_id=self.user.id)
        self.department = Department.objects.create(
            name="Teste Dep", description="Description test dep", owner_id=self.user.id
        )

        self.contract_expired = Contract.objects.create(
            pdf="contracts_pdfs/test.pdf",
            description="Expired contract.",
            amount=10000.00,
            number="C-12345",
            subject="Expired Contract",
            start_date=timezone.now().date() - timezone.timedelta(days=365),
            end_date=timezone.now().date() - timezone.timedelta(days=10),
            department=self.department,
            folder=self.folder,
            owner=self.user,
            status="approved",
            automatic_renewal=False,
            email_sent=False,
        )

        self.contract_due_30_days = Contract.objects.create(
            pdf="contracts_pdfs/test_30_days.pdf",
            description="Contract due in 30 days.",
            amount=15000.00,
            number="C-12346",
            subject="Service Contract",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30),
            department=self.department,
            folder=self.folder,
            owner=self.user,
            status="approved",
            automatic_renewal=False,
            email_sent=False,
        )

        self.contract_due_45_days = Contract.objects.create(
            pdf="contracts_pdfs/test_45_days.pdf",
            description="Contract due in 45 days.",
            amount=20000.00,
            number="C-12347",
            subject="Renewal Contract",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=45),
            department=self.department,
            folder=self.folder,
            owner=self.user,
            status="approved",
            automatic_renewal=True,
            email_sent=False,
        )


    def test_expired_contracts_view(self):
        """
        Test if the expired contracts view returns the correct contracts and template.
        """
        response = self.client.get(reverse("expirations:has_expired_contracts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expired_contracts.html")
        self.assertNotContains(response, self.contract_due_30_days.end_date)
        self.assertNotContains(response, self.contract_due_45_days.end_date)

    def test_contracts_due_in_30_days_view(self):
        """
        Test if the contracts due in 30 days view returns the correct contracts and template.
        """
        response = self.client.get(reverse("expirations:contracts_due_in_30_days"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contracts_due_in_30_days.html")
        self.assertNotContains(response, self.contract_expired.end_date)
        self.assertNotContains(response, self.contract_due_45_days.end_date)

    def test_contracts_due_in_45_days_view(self):
        """
        Test if the contracts due in 45 days view returns the correct contracts and template.
        """
        response = self.client.get(reverse("expirations:contracts_due_in_45_days"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contracts_due_in_45_days.html")
        self.assertNotContains(response, self.contract_expired.end_date)
        self.assertNotContains(response, self.contract_due_30_days.end_date)

    def test_expired_view_no_permission(self):
        """
        Test if the expired view restricts access when the user has no permission.
        """
        self.user = self.User.objects.create_user(
            email="testuser@1234.com", password="password", username='testuser2')
        self.client.login(email="testuser@1234.com", password="password")
        response = self.client.get(reverse("expirations:expired_contracts"))
        self.assertEqual(response.status_code, 302)

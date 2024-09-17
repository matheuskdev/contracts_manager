from django.utils import timezone

from contracts.models import Contract
from departments.models import Department
from folders.models import Folder
from parts.models import Part
from utils.test import SetUpInitial


class ContractModelTest(SetUpInitial):

    def setUp(self):
        super().setUp()
        self.folder = Folder.objects.create(name="Folder1", owner_id=self.user.id)
        self.department = Department.objects.create(
            name="Teste Dep", description="Description test dep", owner_id=self.user.id
        )
        self.contract = Contract.objects.create(
            pdf="contracts_pdfs/test.pdf",
            description="Contrato de prestação de serviços.",
            amount=10000.00,
            number="C-12345",
            subject="Contrato de Serviço",
            start_date=timezone.now().date(),
            department=self.department,
            folder=self.folder,
            owner=self.user,
            contract_type="service",
            status="draft",
        )

    def test_create_contract(self):
        """Test creating a contract with all the necessary fields."""
        self.assertEqual(
            str(self.contract), f"{self.department} - {self.contract.subject}"
        )
        self.assertTrue(self.contract.lgpd)
        self.assertFalse(self.contract.contains_addendum)
        self.assertEqual(self.contract.slug, "contrato-de-servico")

    def test_unique_subject_constraint(self):
        """Tests the uniqueness constraint in the subject field."""
        with self.assertRaises(Exception):
            Contract.objects.create(
                pdf="contracts_pdfs/test2.pdf",
                description="Outro contrato de prestação de serviços.",
                amount=20000.00,
                number="C-12346",
                subject="Contrato de Serviço",  # Mesmo subject
                start_date=timezone.now().date(),
                department=self.department,
                folder=self.folder,
                owner=self.user,
            )

    def test_slug_generation(self):
        """Tests that the slug is generated correctly when not provided."""
        self.assertEqual(self.contract.slug, "contrato-de-servico")

    def test_automatic_renewal(self):
        """Tests whether automatic renewal is configured correctly."""
        contract = Contract.objects.create(
            pdf="contracts_pdfs/test.pdf",
            description="Contrato de prestação de serviços.",
            amount=10000.00,
            number="C-12345",
            subject="Contrato de Serviço com Renovação Automática",
            start_date=timezone.now().date(),
            end_date=None,  # Sem data de término
            department=self.department,
            folder=self.folder,
            owner=self.user,
        )
        self.assertTrue(contract.automatic_renewal)
        self.assertEqual(
            contract.end_date, timezone.now().date() + timezone.timedelta(days=365)
        )

    def test_parts_relationship(self):
        """Tests the ManyToMany relationship with Part."""
        part1 = Part.objects.create(name="Parte A", owner_id=self.user.id)
        part2 = Part.objects.create(name="Parte B", owner_id=self.user.id)

        self.contract.parts.add(part1, part2)

        self.assertEqual(self.contract.parts.count(), 2)
        self.assertIn(part1, self.contract.parts.all())
        self.assertIn(part2, self.contract.parts.all())

    def test_soft_delete(self):
        """Tests the soft delete functionality."""
        self.contract.soft_delete()
        self.assertTrue(self.contract.is_deleted)

    def test_restore(self):
        """Tests restoring a deleted contract."""
        self.contract.restore()
        self.assertFalse(self.contract.is_deleted)

from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from contracts.forms import ContractForm
from contracts.models import Contract
from .test_model import ContractModelTest

class ContractViewTest(ContractModelTest):

    def setUp(self):
        super().setUp()
        self.set_permission(Contract, 'view_contract')
        self.set_permission(Contract, 'add_contract')
        self.set_permission(Contract, 'change_contract')
        self.set_permission(Contract, 'delete_contract')


    def test_list_view_with_contracts(self):
        """Test the Contract list view."""
        response = self.client.get(reverse('contracts:contract_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contrato de Serviço")
        self.assertEqual(len(response.context['contracts']), 1)

    def test_create_contract_view(self):
        """Test the Contract create view."""
        pdf_file = SimpleUploadedFile("test.pdf", b"pdf content", content_type="application/pdf")
        data = {
            'pdf': pdf_file,
            'description': 'New contract',
            'amount': 15000.00,
            'number': 'C-00002',
            'subject': 'New Contract',
            'start_date': timezone.now().date(),
            'department': self.department.id,
            'folder': self.folder.id,
            'owner':self.user.id,
        }
        form = ContractForm(data=data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
        response = self.client.post(reverse('contracts:contract_create'), data)
        print(response.content.decode())
        self.assertEqual(response.status_code, 302)  # Redireciona após criação
        self.assertTrue(Contract.objects.filter(subject='New Contract').exists())
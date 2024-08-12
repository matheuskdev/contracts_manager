from django.test import TestCase
from django.urls import reverse
from .models import Party


class PartyModelTest(TestCase):
    
    def setUp(self):
        self.party = Party.objects.create(
            name="Test Party",
            address="123",
            email="test@example.com",
            phone="1234567890"
        )

    def test_party_creation(self):
        """Test that a Party instance is correctly created."""
        party = self.party
        self.assertEqual(party.name, "Test Party")
        self.assertEqual(party.address, "123")
        self.assertEqual(party.email, "test@example.com")
        self.assertEqual(party.phone, "1234567890")

    def test_party_str_representation(self):
        """Test the __str__ method of the Party model."""
        party = self.party
        self.assertEqual(str(party), "Test Party")

    def test_party_update(self):
        """Test updating an existing Party instance."""
        self.party.name = "Updated Party"
        self.party.save()

        updated_party = Party.objects.get(id=self.party.id)
        self.assertEqual(updated_party.name, "Updated Party")

    def test_party_deletion(self):
        """Test deleting a Party instance."""
        party_id = self.party.id
        self.party.delete()

        with self.assertRaises(Party.DoesNotExist):
            Party.objects.get(id=party_id)

    def test_party_list_view(self):
        """Test the Party list view."""
        response = self.client.get(reverse('party_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.party.name)

    def test_party_detail_view(self):
        """Test the Party detail view."""
        response = self.client.get(reverse('party_detail', kwargs={'pk': self.party.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.party.name)

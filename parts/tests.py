from django.urls import reverse

from .models import Part
from utils.test import SetUpInitial



class PartModelTest(SetUpInitial):

    def setUp(self):
        super().setUp()

        permission = self.set_permission(Part, 'view_part')
        self.user.user_permissions.add(permission)

        self.part = Part.objects.create(
            name="Test Part",
            address="123",
            email="test@example.com",
            phone="1234567890",
            owner=self.user,
        )

    def test_part_creation(self):
        """Test that a Part instance is correctly created."""
        part = self.part
        self.assertEqual(part.name, "Test Part")
        self.assertEqual(part.address, "123")
        self.assertEqual(part.email, "test@example.com")
        self.assertEqual(part.phone, "1234567890")

    def test_part_update(self):
        """Test updating an existing Part instance."""
        self.part.name = "Updated Part"
        self.part.save()

        updated_part = Part.objects.get(id=self.part.id)
        self.assertEqual(updated_part.name, "Updated Part")

    def test_part_deletion(self):
        """Test deleting a Part instance."""
        part_id = self.part.id
        self.part.delete()

        with self.assertRaises(Part.DoesNotExist):
            Part.objects.get(id=part_id)

    def test_part_str_representation(self):
        """Test the __str__ method of the Part model."""
        part = self.part
        self.assertEqual(str(part), "Test Part")

    def test_part_list_view(self):
        """Test the Part list view."""
        response = self.client.get(reverse("parts:part_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part.name)

    def test_part_detail_view(self):
        """Test the Part detail view."""
        response = self.client.get(reverse("parts:part_detail", kwargs={"pk": self.part.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part.name)

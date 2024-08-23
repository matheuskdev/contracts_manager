from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Folder

from utils.test import SetUpInitial

User = get_user_model()


class FolderModelTest(SetUpInitial):

    def setUp(self):
        super().setUp()
        content_type = ContentType.objects.get_for_model(Folder)
        permission, created = Permission.objects.get_or_create(
            codename="view_folder", content_type=content_type
        )
        self.user.user_permissions.add(permission)
        self.client.login(email="testuser@123.com", password="password")

        self.folder = Folder.objects.create(name="Test Folder", owner_id=1)

    def test_folder_creation(self):
        """Test that a Folder instance is correctly created."""
        folder = self.folder
        self.assertEqual(folder.name, "Test Folder")

    def test_folder_str_representation(self):
        """Test the __str__ method of the Folder model."""
        folder = self.folder
        self.assertEqual(str(folder), "Test Folder")

    def test_folder_update(self):
        """Test updating an existing Folder instance."""
        self.folder.name = "Updated Folder"
        self.folder.save()

        updated_folder = Folder.objects.get(id=self.folder.id)
        self.assertEqual(updated_folder.name, "Updated Folder")

    def test_folder_deletion(self):
        """Test deleting a Folder instance."""
        folder_id = self.folder.id
        self.folder.delete()

        with self.assertRaises(Folder.DoesNotExist):
            Folder.objects.get(id=folder_id)



    def test_folder_list_view(self):
        """Test the Folder list view."""
        response = self.client.get(reverse("folders:folder_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.folder.name)

    def test_folder_detail_view(self):
        """Test the Folder detail view."""
        response = self.client.get(reverse("folders:folder_detail", kwargs={"pk": self.folder.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.folder.name)

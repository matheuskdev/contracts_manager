from django.contrib.auth import get_user_model

from django.urls import reverse

from .models import Folder

from utils.test import SetUpInitial

User = get_user_model()


class FolderModelTest(SetUpInitial):

    def setUp(self):
        super().setUp()

        permission = self.set_permission(Folder, 'view_folder')
        self.user.user_permissions.add(permission)
   
        self.folder = Folder.objects.create(name="Test Folder", owner_id=self.user.id)

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

from django.contrib.auth import get_user_model

from utils.test import SetUpInitial

from folders.models import Folder

User = get_user_model()


class FolderModelTest(SetUpInitial):

    def setUp(self):
        super().setUp()

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

from django.urls import reverse

from .test_model import FolderModelTest


class FolderModelTest(FolderModelTest):

    def setUp(self):
        super().setUp()

    def test_folder_permission_list_view(self):
        """Test permission the Folder list view."""
        response = self.client.get(reverse("folders:folder_list"))
        self.assertEqual(response.status_code, 302)

    def test_folder_list_view(self):
        """Test the Folder list view."""
        permission = self.set_permission(self.folder, "view_folder")
        self.user.user_permissions.add(permission)

        response = self.client.get(reverse("folders:folder_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.folder.name)

    def test_folder_detail_view(self):
        """Test the Folder detail view."""
        permission = self.set_permission(self.folder, "view_folder")
        self.user.user_permissions.add(permission)
        response = self.client.get(
            reverse("folders:folder_detail", kwargs={"pk": self.folder.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.folder.name)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

admin.site.site_title = "Admin Contracts Manager"
admin.site.site_header = "Administração do Contracts Manager"
admin.site.index_title = "Bem-vindo a Administração Contracts Manager"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("parts.urls")),
    path("", include("folders.urls")),
    path("", include("contracts.urls")),
    path("", include("addendums.urls")),
    path("", include("evaluations.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

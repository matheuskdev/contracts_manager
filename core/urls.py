from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

admin.site.site_title = "Admin Contracts Manager"
admin.site.site_header = "Administração do Contracts Manager"
admin.site.index_title = "Bem-vindo a Administração do Contracts Manager"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),

    path('', include('parts.urls')),
]

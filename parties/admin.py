from django.contrib import admin
from .models import Party
from . import forms

class PartyAdmin(admin.ModelAdmin):
    form = forms.PartyForm
    list_display = ('name', 'address', 'email', 'phone', 'created_at', 'updated_at', 'owner')
    search_fields = ('name',)
    list_filter = ('name', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'address', 'email', 'phone')}),
        ('Datas', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

admin.site.register(Party, PartyAdmin)

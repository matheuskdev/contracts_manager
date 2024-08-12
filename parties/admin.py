from django.contrib import admin
from . import models


class PartyAdmin(admin.ModelAdmin):
    lis_display = ('name', 'address', 'email', 'phone',)
    search_fields = ('name',)

admin.site.register(models.Party, PartyAdmin)
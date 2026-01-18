from django.contrib import admin
from .models import Birthday


class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    date_hierarchy = 'birth_date'

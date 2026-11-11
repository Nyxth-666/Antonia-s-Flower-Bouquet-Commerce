from django.contrib import admin
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):

    list_display = ('last_name', 'first_name', 'email', 'time_of_entry')
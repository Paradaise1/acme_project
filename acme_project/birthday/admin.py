from django.contrib import admin

from .models import Birthday


admin.site.empty_value_display = 'Не задано'

admin.site.register(Birthday)

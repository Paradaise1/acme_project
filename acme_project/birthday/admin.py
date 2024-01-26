from django.contrib import admin

from .models import Birthday, Tag


admin.site.empty_value_display = 'Не задано'

admin.site.register(Birthday)
admin.site.register(Tag)

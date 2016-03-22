from django.contrib import admin
from .models import TextFilter, TextFormat


class FilterInline(admin.TabularInline):
    model = TextFilter
    ordering = ('sort',)
    extra = 1


class FormatAdmin(admin.ModelAdmin):
    inlines = [FilterInline]
    prepopulated_fields = {
        'slug': ('name',),
    }


admin.site.register(TextFormat, FormatAdmin)

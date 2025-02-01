# faqs/admin.py

from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
  list_display = ('question', 'created_at', 'updated_at', 'is_active')
  list_filter = ('is_active', 'created_at', 'updated_at')
  search_fields = ('question', 'answer', 'question_hi', 'question_bn')
  readonly_fields = ('created_at', 'updated_at')

  fieldsets = (
    ('English Content', {
      'fields': ('question', 'answer')
    }),
    ('Hindi Translation', {
      'fields': ('question_hi', 'answer_hi'),
      'classes': ('collapse',)
    }),
    ('Bengali Translation', {
      'fields': ('question_bn', 'answer_bn'),
      'classes': ('collapse',)
    }),
    ('Metadata', {
      'fields': ('is_active', 'created_at', 'updated_at'),
      'classes': ('collapse',)
    }),
  )

  def has_delete_permission(self, request, obj=None):
    return request.user.is_superuser
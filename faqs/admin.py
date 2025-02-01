# faqs/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
  list_display = ('question_preview', 'languages_available', 'created_at', 'updated_at', 'is_active')
  list_filter = ('is_active', 'created_at', 'updated_at')
  search_fields = ('question', 'answer', 'question_hi', 'question_bn')
  readonly_fields = ('created_at', 'updated_at')

  fieldsets = (
    ('English Content', {
      'fields': ('question', 'answer'),
      'description': 'Enter the FAQ content in English (required)'
    }),
    ('Hindi Translation', {
      'fields': ('question_hi', 'answer_hi'),
      'classes': ('collapse',),
      'description': 'Enter the hindi translation (optional)'
    }),
    ('Bengali Translation', {
      'fields': ('question_bn', 'answer_bn'),
      'classes': ('collapse',),
      'description': 'Enter the bengali translation (optional)'
    }),
    ('Metadata', {
      'fields': ('is_active', 'created_at', 'updated_at'),
      'classes': ('collapse',)
    }),
  )

  def question_preview(self, obj):
    """Display truncated question in list view"""
    return obj.question[:100] + '...' if len(obj.question) > 100 else obj.question
  question_preview.short_description = 'Question'

  def languages_available(self, obj):
    """Display available translation"""
    languages = ['English']
    if obj.question_hi and obj.answer_hi:
      languages.append('Hindi')
    if obj.question_bn and obj.answer_bn:
      languages.append('Bengali')

    return format_html('<br>'.join(languages))
  languages_available.short_description = 'Available Languages'

  class Media:
    css = {
      'all': ('admin/css/custom_admin.css',)
    }
    js = ('admin/js/custom_admin.js',)

  def save_model(self, req, obj, form, change):
    """Override save model to handle any pre-save processing"""
    super().save_model(req, obj, form, change)

  def has_delete_permission(self, request, obj=None):
    return request.user.is_superuser
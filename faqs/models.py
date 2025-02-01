# faqs/models.py

from django.db import models
from django.core.cache import cache
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

class FAQ(models.Model):
  # Base field english
  question = models.TextField(_('Question (English)'))
  answer = RichTextField(_('Answer (English)'))

  # Hindi translation
  question_hi = models.TextField(_('Question (Hindi)'), blank=True, null=True)
  answer_hi = RichTextField(_('Answer (Hindi)'), blank=True, null=True)

  # Bengali translation
  question_bn = models.TextField(_('Question (Bengali)'), blank=True, null=True)
  answer_bn = RichTextField(_('Answer (Bengali)'), blank=True, null=True)

  # Metadata
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)

  class Meta:
    verbose_name = 'FAQ'
    verbose_name_plural = 'FAQs'
    ordering = ['-created_at']

  def __str__(self):
    return self.question[:100]

  def get_cached_translation(self, field_name, lang):
    """Get cached translation for a field"""
    cache_key = f'faq_{self.id}_{field_name}_{lang}'
    cached_value = cache.get(cache_key)

    if cached_value is None:
      translated_field = getattr(self, f'{field_name}_{lang}', None)
      if translated_field:
        cache.set(cache_key, translated_field, timeout=3600) # Cache for 1 hour
        return translated_field
      return getattr(self, field_name) # Fallback to english if the other language does not exist

    return cached_value

  def get_question(self, lang='en'):
    """Get questions in a specified language"""
    if lang == 'en':
      return self.question

    return self.get_cached_translation('question', lang)

  def get_answer(self, lang='en'):
    """Get answer in specified language"""
    if lang == 'en':
      return self.answer

    return self.get_cached_translation('answer', lang)

  def to_dict(self, lang='en'):
    """Convert FAQ to dictionary with translations"""
    return {
      'id': self.id,
      'question': self.get_question(lang),
      'answer': self.get_answer(lang),
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }
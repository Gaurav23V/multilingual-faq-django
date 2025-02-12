# faqs/models.py

from django.db import models
from django.conf import settings
from django.core.cache import cache
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from .utils import TranslationService

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

  def save(self, *args, **kwargs):
    # Check if the object is new or being updated
    is_new = self._state.adding

    # If new, proceed to generate translations before the first save
    if is_new:
        # Initialize translation service
        translator = TranslationService()

        # Generate translations
        try:
            self.question_hi = translator.translate_text(self.question, 'hi')
            self.answer_hi = translator.translate_html(self.answer, 'hi')
        except Exception as e:
            logger.error(f"Hindi translation failed: {str(e)}")
            self.question_hi = self.question  # Fallback to English
            self.answer_hi = self.answer

        try:
            self.question_bn = translator.translate_text(self.question, 'bn')
            self.answer_bn = translator.translate_html(self.answer, 'bn')
        except Exception as e:
            logger.error(f"Bengali translation failed: {str(e)}")
            self.question_bn = self.question  # Fallback to English
            self.answer_bn = self.answer

    # Clear cache before saving
    self.clear_cache()

    # Save the object once
    super().save(*args, **kwargs)

  def clear_cache(self):
    """Clear all cached version of this FAQ"""
    languages = ['en', 'hi', 'bn']
    for lang in languages:
      cache.delete(f'faq_{self.id}_question_{lang}')
      cache.delete(f'faq_{self.id}_answer_{lang}')
      cache.delete(f'faq_list_{lang}')
      cache.delete(f'faq_detail_{self.id}_{lang}')

  def get_cached_translation(self, field_name, lang):
    """Get cached translation for a field"""
    cache_key = f'faq_{self.id}_{field_name}_{lang}'
    cached_value = cache.get(cache_key)

    if cached_value is None:
        if lang == 'en':
            value = getattr(self, field_name)
        else:
          translation_field = f'{field_name}_{lang}'
          if hasattr(self, translation_field):
              value = getattr(self, translation_field)
              if not value:  # Fallback to english if translation is not available
                  value = getattr(self, field_name)
          else:
            value = getattr(self, field_name)
            
        cache.set(cache_key, value, timeout=settings.CACHE_TTL)
        return value

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
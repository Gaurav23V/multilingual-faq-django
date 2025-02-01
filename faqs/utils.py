# faqs/utils.py

from googletrans import Translator
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


class TranslationService:
  def __init__(self):
    self.translator = Translator()
    self.supported_languages = {'hi': 'hindi', 'bn': 'bengali'}

  def translate_text(self, text, target_lang):
    """
    Translate text to the target language
    """
    try:
      if not text:
        return None

      translation = self.translator.translate(
        text,
        dest=target_lang
      )

      return translation.text
    except Exception as e:
      logger.error(f"Translation error: {str(e)}")
      return None

  def translate_html(self, html_content, target_lang):
    """
    Translate HTML content while preserving HTML tags
    """
    try:
      if not html_content:
        return None

      # Simple HTML preservation for now
      translation = self.translator.translate(
        html_content,
        dest=target_lang
      )
      return translation.text
    except Exception as e:
      logger.error(f"HTML translation error: {str(e)}")
      return None
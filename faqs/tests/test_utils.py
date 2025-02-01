# faqs/tests/test_utils.py

import pytest
from faqs.utils import TranslationService

class TestTranslationService:
    @pytest.fixture
    def translator(self):
        return TranslationService()

    def test_translate_text(self, translator):
        """Test basic text translation"""
        text = "Hello"
        translated = translator.translate_text(text, 'hi')
        assert translated is not None
        assert translated != text

    def test_translate_html(self, translator):
        """Test HTML content translation"""
        html = "<p>Hello</p>"
        translated = translator.translate_html(html, 'hi')
        assert translated is not None
        assert '<p>' in translated

    def test_empty_text_translation(self, translator):
        """Test handling of empty text"""
        assert translator.translate_text('', 'hi') is None
        assert translator.translate_html('', 'hi') is None

    def test_invalid_language_code(self, translator):
        """Test handling of invalid language codes"""
        with pytest.raises(Exception):
            translator.translate_text("Hello", 'invalid_code')
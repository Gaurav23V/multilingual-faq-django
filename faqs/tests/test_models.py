# faqs/tests/test_models.py

import pytest
from django.core.cache import cache
from faqs.models import FAQ
from django.test import override_settings

pytestmark = pytest.mark.django_db

class TestFAQModel:
    def test_faq_creation(self, sample_faq):
        """Test that FAQ can be created with basic fields"""
        assert isinstance(sample_faq, FAQ)
        assert str(sample_faq) == "What is this service?"

    def test_automatic_translation_on_create(self):
        """Test that translations are automatically generated on creation"""
        faq = FAQ.objects.create(
            question="Hello, how are you?",
            answer="<p>I am fine, thank you.</p>"
        )
        # Check if translations were generated
        assert faq.question_hi is not None
        assert faq.question_bn is not None
        assert faq.answer_hi is not None
        assert faq.answer_bn is not None

    def test_get_question_with_translation(self, sample_faq):
        """Test getting question in different languages"""
        assert sample_faq.get_question('en') == "What is this service?"
        assert sample_faq.get_question('hi') == "यह सेवा क्या है?"
        assert sample_faq.get_question('bn') == "এই সেবাটি কি?"

    def test_get_answer_with_translation(self, sample_faq):
        """Test getting answer in different languages"""
        assert sample_faq.get_answer('en') == "<p>This is a test service.</p>"
        assert sample_faq.get_answer('hi') == "<p>यह एक परीक्षण सेवा है।</p>"
        assert sample_faq.get_answer('bn') == "<p>এটি একটি পরীক্ষা পরিষেবা।</p>"

    def test_fallback_to_english(self, faq_without_translations):
        """Test fallback to English when translation is not available"""
        question = "Question without translation"
        assert faq_without_translations.get_question('hi') == question
        assert faq_without_translations.get_question('bn') == question

    @override_settings(CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    })
    def test_caching_mechanism(self, sample_faq):
        """Test that translations are properly cached"""
        # Clear cache first
        cache.clear()

        # First call should cache the result
        question_hi = sample_faq.get_question('hi')
        cache_key = f'faq_{sample_faq.id}_question_hi'

        # Verify cache was set
        assert cache.get(cache_key) == question_hi

        # Modify directly in database to verify cache is used
        sample_faq.question_hi = "Changed question"
        sample_faq.save()

        # Should still get cached version
        assert sample_faq.get_question('hi') == question_hi

        # Clear cache and verify new version is retrieved
        cache.clear()
        assert sample_faq.get_question('hi') == "Changed question"

    def test_clear_cache(self, sample_faq):
        """Test that clear_cache removes all cached versions"""
        # Set some cached values
        sample_faq.get_question('hi')
        sample_faq.get_question('bn')

        # Clear cache
        sample_faq.clear_cache()

        # Verify cache was cleared
        cache_key = f'faq_{sample_faq.id}_question_hi'
        assert cache.get(cache_key) is None
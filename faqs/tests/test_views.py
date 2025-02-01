# faqs/tests/test_views.py

import pytest
from django.urls import reverse
from rest_framework import status
from django.core.cache import cache

pytestmark = pytest.mark.django_db

class TestFAQViewSet:
    def test_list_faqs(self, api_client, sample_faq):
        """Test listing FAQs returns correct data"""
        url = reverse('faq-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['question'] == sample_faq.question

    def test_list_faqs_with_language(self, api_client, sample_faq):
        """Test listing FAQs with different languages"""
        url = reverse('faq-list')

        # Test Hindi
        response = api_client.get(f"{url}?lang=hi")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['question'] == sample_faq.question_hi

        # Test Bengali
        response = api_client.get(f"{url}?lang=bn")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['question'] == sample_faq.question_bn

    def test_retrieve_faq(self, api_client, sample_faq):
        """Test retrieving single FAQ"""
        url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['question'] == sample_faq.question

    def test_retrieve_faq_with_language(self, api_client, sample_faq):
        """Test retrieving single FAQ with different languages"""
        url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})

        # Test Hindi
        response = api_client.get(f"{url}?lang=hi")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['question'] == sample_faq.question_hi

        # Test Bengali
        response = api_client.get(f"{url}?lang=bn")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['question'] == sample_faq.question_bn

    def test_invalid_language_code(self, api_client, sample_faq):
        """Test behavior with invalid language code"""
        url = reverse('faq-list')
        response = api_client.get(f"{url}?lang=invalid")

        assert response.status_code == status.HTTP_200_OK
        # Should fallback to English
        assert response.data['results'][0]['question'] == sample_faq.question

    @pytest.mark.django_db(transaction=True)
    def test_api_caching(self, api_client, sample_faq):
        """Test that API responses are cached"""
        cache.clear()
        url = reverse('faq-list')

        # First request should cache the response
        response1 = api_client.get(f"{url}?lang=hi")

        # Modify the FAQ
        sample_faq.question_hi = "Changed question"
        sample_faq.save()

        # Second request should return cached response
        response2 = api_client.get(f"{url}?lang=hi")

        assert response1.data == response2.data
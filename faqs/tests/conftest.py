# faqs/tests/conftest.py

import pytest
from faqs.models import FAQ
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
  return APIClient()


@pytest.fixture
def sample_faq():
  faq = FAQ.objects.create(
    question="What is this service?",
    answer="<p>This is a test service.</p>",
    question_hi="यह सेवा क्या है?",
    answer_hi="<p>यह एक परीक्षण सेवा है।</p>",
    question_bn="এই সেবাটি কি?",
    answer_bn="<p>এটি একটি পরীক্ষা পরিষেবা।</p>"
  )
  return faq

@pytest.fixture
def faq_without_translations():
  return FAQ.objects.create(
    question = 'Question without translation',
    answer = '<p>Answer without translation</p>'
  )
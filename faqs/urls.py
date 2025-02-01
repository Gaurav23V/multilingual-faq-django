# faqs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet

router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faq')

app_name = 'faqs'

urlpatterns = [
  path('', include(router.urls)),
]
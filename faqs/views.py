# faqs/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = FAQ.objects.filter(is_active=True)
  serializer_class = FAQSerializer

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['lang'] = self.request.query_params.get('lang', 'en')
    return context

  def list(self, req, *args, **kwargs):
    lang = req.query_params.get('lang', 'en')
    cache_key = f'faq_list_{lang}'

    # Try to get cached responses
    cached_response = cache.get(cache_key)
    if cached_response:
      return Response(cached_response)

    # If not cached then generate the response
    queryset = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(queryset, many=True)
    response_data = serializer.data

    # Cache the response for 1 hour
    cache.set(cache_key, response_data, timeout=3600)

    return Response(response_data)

  def retrieve(self, req, *args, **kwargs):
    lang = req.query_params.get('lang', 'en')
    instance = self.get_object()
    cache_key = f'faq_detail_{instance.id}_{lang}'

    # Try to get the cached response
    cached_response = cache.get(cache_key)
    if cached_response:
      return Response(cached_response)

    # If not present in cache, we generate a response
    serializer = self.get_serializer(instance)
    response_data = serializer.data

    # Cache the response for an hour
    cache.set(cache_key, response_data, timeout=3600)

    return Response(response_data)
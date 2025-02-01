from django.urls import path
from .views import FAQView


urlpatterns = [
    path('api/faqs/', FAQView.as_view(), name='faq-list'),
    path("api/faqs/<int:faq_id>/", FAQView.as_view(), name="faq-detail"),
]

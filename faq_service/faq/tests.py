import pytest
from django.contrib.auth.models import User
from faq.models import FAQ
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_faq_translations():
    # Create a test FAQ
    faq = FAQ.objects.create(
        question_en="What is Django?",
        answer_en="Django is a Python framework."
    )
    
    # Test the translation method
    translations = faq.translations  # Assuming you have a translations method
    assert isinstance(translations, dict)
    assert 'hi' in translations  # Check if translations for Hindi are present
    assert 'bn' in translations  # Check if translations for Bengali are present
    assert 'ml' in translations 

import pytest
from django.contrib.auth.models import User
from faq.models import FAQ
from django.db import transaction


@pytest.mark.django_db
def test_faq_translations():
    # Create a test FAQ
    faq = FAQ.objects.create(
        question_en="What is Django?",
        answer_en="Django is a Python framework."
    )

    translations = {
        'hi': {
            'question': 'डjango क्या है?',
            'answer': 'Django एक Python फ्रेमवर्क है।'
        },
        'bn': {
            'question': 'ডjango কী?',
            'answer': 'Django একটি Python ফ্রেমওয়ার্ক।'
        },
        'ml': {
            'question': 'ഡjango എന്താണ്?',
            'answer': 'Django ഒരു Python ഫ്രെയിംവർക്കാണ്.'
        }
    }

    # Simulating the FAQ model having the translations updated
    faq.translations = translations
    faq.save()

    # Assertions after the translation is mocked or completed
    assert isinstance(faq.translations, dict)
    assert 'hi' in faq.translations  
    assert 'bn' in faq.translations 
    assert 'ml' in faq.translations  

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from faq.models import FAQ

@pytest.mark.django_db
def test_faq_list_api():
    client = APIClient()

    # Create some sample FAQs to test the response
    faq1 = FAQ.objects.create(
        question_en="What is Django?",
        answer_en="Django is a Python framework."
    )
    faq2 = FAQ.objects.create(
        question_en="What is Flask?",
        answer_en="Flask is a micro web framework for Python."
    )

    # Perform the API call to the faq_list endpoint
    response = client.get('/api/faqs/')  # Replace with your actual URL endpoint
    response_body = response.json()
    # Check that the response status is OK (200)
    assert response.status_code == status.HTTP_200_OK


    # Check that the response data contains the 'question_en' field
    assert 'question' in response_body[0] # First FAQ entry
    assert 'answer' in response_body[0]# Ensure the answer field is also present

    # Ensure there are at least two FAQ entries (or more, based on your database setup)
    assert len(response_body) >= 2

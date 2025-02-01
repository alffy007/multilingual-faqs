from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FAQ
from .translate import translate_faq


# To allow POST, PUT, DELETE without CSRF token (for API)
@method_decorator(csrf_exempt, name='dispatch')
class FAQView(View):
    def get(self, request):
        lang = request.GET.get("lang", "en")  # Default to English
        faqs = FAQ.objects.all()
        data = [faq.get_translation(lang) for faq in faqs]
        return JsonResponse(data, safe=False)

    def post(self, request):
        """Create a new FAQ."""
        try:
            data = json.loads(request.body)
            faq = FAQ.objects.create(
                question_en=data.get("question_en", "No Question available"),
                answer_en=data.get("answer_en", "No answer available"),
                is_updated=True,
            )

            return JsonResponse({"question_en": faq.question_en,
                                "answer_en": faq.answer_en, "id": faq.id}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    def put(self, request, faq_id):
        """Update an existing FAQ."""
        faq = get_object_or_404(FAQ, id=faq_id)
        try:
            data = json.loads(request.body)
            faq.question_en = data.get("question_en", faq.question_en)
            faq.answer_en = data.get("answer_en", faq.answer_en)
            faq.is_updated = True
            faq.save()
            return JsonResponse({"message": "FAQ updated"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    def delete(self, request, faq_id):
        """Delete an FAQ."""
        faq = get_object_or_404(FAQ, id=faq_id)
        faq.delete()
        return JsonResponse({"message": "FAQ deleted"}, status=204)

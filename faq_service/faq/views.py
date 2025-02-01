from django.http import JsonResponse
from django.views import View
from .models import FAQ

class FAQView(View):
    def get(self, request):
        lang = request.GET.get('lang', 'en')  # Default to English
        faqs = FAQ.objects.all()
        data = [faq.get_translation(lang) for faq in faqs]
        return JsonResponse(data, safe=False)




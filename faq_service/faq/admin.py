from django.contrib import admin
from faq.models import FAQ


@admin.register(FAQ)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question_en', 'answer_en']
    search_fields = ['question_en']
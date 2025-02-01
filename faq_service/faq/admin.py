from django.contrib import admin
from .models import FAQ


class FAQAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }

    list_display = ('question_en', 'is_updated', 'translations')
    search_fields = ['question_en', 'answer_en']
    list_filter = ['is_updated']
    fields = ('question_en', 'answer_en', 'translations', 'is_updated')
    readonly_fields = ('translations',)


admin.site.register(FAQ, FAQAdmin)

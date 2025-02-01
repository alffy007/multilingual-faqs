from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from faq.translate import translate_faq
from django.core.cache import cache
import logging


logger = logging.getLogger('django.core.cache')
class FAQ(models.Model):
    question_en = models.TextField(
        default="No Question available", help_text="Enter your question in English"
    )
    answer_en = RichTextField(
        default="No answer available", blank=True, help_text="Enter your answer in English"
    )
    translations = models.JSONField(default=dict, blank=True)
    is_updated = models.BooleanField(default=True, help_text="Flag indicating if the FAQ content has been updated")

    def save(self, *args, **kwargs):
        cache.delete(f"faq_translation_{self.id}_en")
        for lang in self.translations:
            cache.delete(f"faq_translation_{self.id}_{lang}")
        super().save(*args, **kwargs)
        translate_faq.delay(self.id)

    def get_translation(self, lang="en"):
        cache_key = f"faq_translation_{self.id}_{lang}"
        cached_translation = cache.get(cache_key)

        if cached_translation:
            logger.info(f"Cache hit for {cache_key}")
            return cached_translation
        else:
            logger.info(f"Cache miss for {cache_key}")
        if lang == "en":
            translation = {"question": self.question_en, "answer": self.answer_en}
        else:
            translation = self.translations.get(lang, {"question": self.question_en, "answer": self.answer_en})

        cache.set(cache_key, translation, timeout=60)
        logger.info(f"Cache set for {cache_key}")
        return translation

    def __str__(self):
        return self.question_en
    

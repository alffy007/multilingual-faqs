from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from faq.tasks import translate_faq 


class FAQ(models.Model):
    question_en = models.TextField(default="No Question available", help_text="Enter your question in English")
    answer_en = RichTextField(default="No answer available", blank=True, help_text="Enter your answer in English")
    translations = models.JSONField(default=dict, blank=True)

    def save(self, *args, **kwargs) :
        super().save(*args, **kwargs)
        translate_faq.delay(self.id) 

    def get_translation(self, lang="en"):
        if lang == "en":
            return {"question": self.question_en, "answer": self.answer_en}

        return self.translations.get(lang, {"question": self.question_en, "answer": self.answer_en})

    def __str__(self):
        return self.question_en

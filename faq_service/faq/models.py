from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    question_hi = models.TextField(null=True, blank=True)  # Hindi translation
    question_bn = models.TextField(null=True, blank=True)  # Bengali translation

    def get_translated_question(self, lang='en'):
        return getattr(self, f'question_{lang}', self.question)
    
    def __str__(self):
        return self.question
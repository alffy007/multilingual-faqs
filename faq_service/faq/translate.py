import asyncio
import logging
from celery import shared_task
from googletrans import Translator

# Initialize logger
logger = logging.getLogger(__name__)



# Asynchronous function to translate text to the specified language
async def translate_text(text: str, dest_lang: str) -> str:
    try:
        translator = Translator()
        translation = await translator.translate(text, dest=dest_lang)
        return translation.text
    except Exception as exc:
        logger.error('Translation error: %s', str(exc))
        raise



# Celery task to translate FAQ
@shared_task(bind=True, max_retries=3)
def translate_faq(self, faq_id: int):
    from faq.models import FAQ

    try:
        # Fetch the FAQ object by ID
        faq = FAQ.objects.filter(id=faq_id).first()
        if not faq:
            logger.error('FAQ %d not found', faq_id)
            return None

        logger.info(
            'Starting translation for FAQ %d: %s',
            faq_id,
            faq.question_en
        )

        # List of target languages
        languages = ['hi', 'bn', 'ml']
        translations_dict = {}

        # Check if the FAQ needs to be updated
        if not faq.is_updated:
            logger.info(
                f"FAQ {faq_id} already translated, skipping translation.")
            return None

        # Create a new event loop for asynchronous tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Asynchronous function to process translations
            async def process_translations() -> None:
                for lang in languages:
                    question_task = translate_text(faq.question_en, lang)
                    answer_task = translate_text(faq.answer_en, lang)
                    translated_question, translated_answer = await asyncio.gather(
                        question_task,
                        answer_task,
                        return_exceptions=True
                    )

                    # Check for translation errors
                    for result in [translated_question, translated_answer]:
                        if isinstance(result, Exception):
                            logger.error(
                                f"Translation failed for language {lang}: {result}")
                            return

                    logger.info(f'Completed translation to {lang}')
                    translations_dict[lang] = {
                        'question': translated_question,
                        'answer': translated_answer
                    }

        finally:
            # Run the asynchronous translation process
            loop.run_until_complete(process_translations())
            loop.close()

        # Update FAQ translations if new translations are available
        if translations_dict:
            current_translations = faq.translations or {}
            current_translations.update(translations_dict)
            faq.translations = current_translations
            faq.is_updated = False
            faq.save(update_fields=['translations', 'is_updated'])

        logger.info('Successfully saved translations for FAQ %d', faq_id)
        return translations_dict

    except Exception as exc:
        logger.error(f'Translation failed: {exc}')
        retry_countdown = 2 ** self.request.retries
        self.retry(exc=exc, countdown=retry_countdown)

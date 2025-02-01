import asyncio
import logging
from celery import shared_task
from googletrans import Translator

logger = logging.getLogger(__name__)

async def translate_text(text: str, dest_lang: str) -> str:
    """Translate text to the target language asynchronously."""
    try:
        translator = Translator()
        translation = await translator.translate(text, dest=dest_lang)
        return translation.text
    except Exception as exc:
        logger.error('Translation error: %s', str(exc))
        raise

@shared_task(bind=True, max_retries=3)
def translate_faq(self, faq_id: int) :
    """Translate FAQ content to multiple languages."""
    from faq.models import FAQ

    try:
        faq = FAQ.objects.filter(id=faq_id).first()
        if not faq:
            logger.error('FAQ %d not found', faq_id)
            return None

        logger.info(
            'Starting translation for FAQ %d: %s',
            faq_id,
            faq.question_en
        )

        languages = ['hi', 'bn', 'ml']  # Add more languages as needed
        translations_dict = {}

        # Only proceed if `is_updated` is True (indicating updates)
        if not faq.is_updated:
            logger.info(f"FAQ {faq_id} already translated, skipping translation.")
            return None  # Skip translation if it's already done

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            async def process_translations() -> None:
                """Process translations for all target languages."""
                for lang in languages:
                    # Translate each FAQ content
                    question_task = translate_text(faq.question_en, lang)
                    answer_task = translate_text(faq.answer_en, lang)
                    translated_question, translated_answer = await asyncio.gather(
                        question_task,
                        answer_task,
                        return_exceptions=True
                    )

                    # Handle any exceptions that occurred during translation
                    for result in [translated_question, translated_answer]:
                        if isinstance(result, Exception):
                            logger.error(f"Translation failed for language {lang}: {result}")
                            return  # Stop and return if translation fails

                    logger.info(f'Completed translation to {lang}')
                    translations_dict[lang] = {
                        'question': translated_question,
                        'answer': translated_answer
                    }

        finally:
            loop.run_until_complete(process_translations())
            loop.close()

        # After translations are done, save them in the FAQ model
        if translations_dict:
            current_translations = faq.translations or {}
            current_translations.update(translations_dict)
            faq.translations = current_translations

            # Save translations and set `is_updated` to False after the translations
            faq.is_updated = False
            faq.save(update_fields=['translations', 'is_updated'])

        logger.info('Successfully saved translations for FAQ %d', faq_id)
        return translations_dict

    except Exception as exc:
        logger.error(f'Translation failed: {exc}')
        retry_countdown = 2 ** self.request.retries
        self.retry(exc=exc, countdown=retry_countdown)

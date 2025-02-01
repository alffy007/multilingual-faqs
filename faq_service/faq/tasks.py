from celery import shared_task
from googletrans import Translator
import asyncio


# Define the async translation function
async def translate_text(text, dest_lang):
    translator = Translator()
    translation = await translator.translate(text, dest=dest_lang)
    return translation.text

@shared_task
def translate_faq(faq_id):
    from faq.models import FAQ
    # Get or create the event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Fetch the FAQ object
    faq = FAQ.objects.get(id=faq_id)
    print(f"Translating FAQ: {faq.question_en}")  # Debugging purposes

    # Define languages to translate into
    languages = ["hi", "bn"]
    translations_dict = {}

    # Perform translations
    for lang in languages:
        try:
            translated_question = loop.run_until_complete(translate_text(faq.question_en, lang))
            translated_answer = loop.run_until_complete(translate_text(faq.answer_en, lang))
            print(f"Translated to {lang}: {translated_question}")  # Debugging purposes
            translations_dict[lang] = {
                "question": translated_question if translated_question else faq.question_en,
                "answer": translated_answer if translated_answer else faq.answer_en,
            }
        except Exception as e:
            print(f"Translation failed for {lang}: {e}")  # Debugging purposes
            translations_dict[lang] = {
                "question": faq.question_en,
                "answer": faq.answer_en,
            }

    # Save translations to the FAQ object
    faq.translations = translations_dict
    faq.save(update_fields=["translations"])  # Save only the translations field
from googletrans import Translator

translator = Translator()

def translate_caption(text):
    translations = {}
    try:
        translations["Hindi"] = translator.translate(text, dest='hi').text
        translations["Gujarati"] = translator.translate(text, dest='gu').text
        translations["Marathi"] = translator.translate(text, dest='mr').text
        translations["Malayalam"] = translator.translate(text, dest='ml').text
        translations["French"] = translator.translate(text, dest='fr').text
        translations["German"] = translator.translate(text, dest='de').text
    except Exception as e:
        translations["error"] = str(e)
    return translations

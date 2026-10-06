from deep_translator import GoogleTranslator, MyMemoryTranslator


class Translator:
    def translate(self, text):
        raise NotImplementedError("Translator must implement the translate method.")


class GoogleTranslatorAdapter(Translator):
    def __init__(self, source="auto", target="pt"):
        self.translator = GoogleTranslator(source=source, target=target)

    def translate(self, text):
        return self.translator.translate(text)

class MyMemoryTranslatorAdapter(Translator):
    def __init__(self, source="auto", target="pt"):
        self.translator = MyMemoryTranslator(source=source, target=target)

    def translate(self, text):
        return self.translator.translate(text)

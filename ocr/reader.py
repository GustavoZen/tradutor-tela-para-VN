import pytesseract
from PIL import ImageOps


class OCRReader:
    def read(self, image):
        raise NotImplementedError("OCR reader must implement the read method.")


class TesseractReader(OCRReader):
    def __init__(self, lang="eng"):
        self.lang = lang

    def read(self, image):
        # Tons de cinza + ampliação ajudam o Tesseract com textos pequenos de tela
        image = ImageOps.grayscale(image)
        image = image.resize((image.width * 2, image.height * 2))

        text = pytesseract.image_to_string(image, lang=self.lang)

        return text.strip()

import sys
from pathlib import Path

import pytesseract
from PIL import ImageOps


def find_bundled_tesseract():
    # No executável (PyInstaller), sys.frozen existe e o .exe fica em sys.executable.
    # Rodando pelo Python, usa a raiz do projeto.
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent.parent

    bundled = app_dir / "Tesseract-OCR" / "tesseract.exe"

    return bundled if bundled.exists() else None


# Se houver um Tesseract junto do programa, usa ele; senão, procura no PATH
bundled_tesseract = find_bundled_tesseract()

if bundled_tesseract:
    pytesseract.pytesseract.tesseract_cmd = str(bundled_tesseract)


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

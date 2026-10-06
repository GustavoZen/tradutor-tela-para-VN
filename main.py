import queue
import threading
import time

from screen.selector import select_screen_area
from screen.capture import capture_region
from ocr.reader import TesseractReader
from translation.translator import GoogleTranslatorAdapter, MyMemoryTranslatorAdapter
from ui.overlay import TranslationOverlay


def watch_region(x, y, width, height, reader, translator, results, interval=1.0):
    last_text = ""

    while True:
        image = capture_region(x, y, width, height)

        # Junta as linhas e remove espaços extras: evita traduzir de novo
        # só porque o OCR quebrou a linha diferente
        text = " ".join(reader.read(image).split())

        if text and text != last_text:
            last_text = text

            try:
                results.put(translator.translate(text))
            except Exception as error:
                results.put(f"Erro na tradução: {error}")

        time.sleep(interval)


def main():
    result = select_screen_area()

    if result is None:
        print("Nenhuma área foi selecionada.")
        return

    screen_width, screen_height, x, y, width, height = result

    reader = TesseractReader(lang="eng")
    translator = MyMemoryTranslatorAdapter(source="en-US", target="pt-BR")
    results = queue.Queue()

    # daemon=True: a thread termina junto com o programa quando a janela fecha
    worker = threading.Thread(
        target=watch_region,
        args=(x, y, width, height, reader, translator, results),
        daemon=True
    )
    worker.start()

    # A janela fica logo acima da área (borda de baixo em y - 5),
    # para não entrar na própria captura
    overlay = TranslationOverlay(x, y - 5, width)
    overlay.run(results)


if __name__ == "__main__":
    main()

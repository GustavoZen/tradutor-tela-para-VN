from screen.selector import select_screen_area
from screen.capture import capture_region
from ocr.reader import TesseractReader


def main():
    result = select_screen_area()

    if result is None:
        print("Nenhuma área foi selecionada.")
        return

    screen_width, screen_height, x, y, width, height = result

    print(f"Screen: {screen_width}x{screen_height}")
    print(f"Area: x={x}, y={y}, width={width}, height={height}")

    image = capture_region(x, y, width, height)

    image.save("capture.png")

    print("Captura salva em capture.png")

    reader = TesseractReader(lang="eng")
    text = reader.read(image)

    print("Texto reconhecido:")
    print(text if text else "(nenhum texto encontrado)")


if __name__ == "__main__":
    main()

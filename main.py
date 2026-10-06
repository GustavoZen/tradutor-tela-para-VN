from screen.selector import select_screen_area


def main():
    result = select_screen_area()

    if result is None:
        print("Nenhuma área foi selecionada.")
        return

    screen_width, screen_height, x, y, width, height = result

    print(f"Screen: {screen_width}x{screen_height}")
    print(f"Area: x={x}, y={y}, width={width}, height={height}")


if __name__ == "__main__":
    main()
    #Próximos passos
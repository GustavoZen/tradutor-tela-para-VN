import tkinter as tk


def select_screen_area():
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    result = None
    start_x = 0
    start_y = 0
    selection = None

    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.configure(background="black")
    root.config(cursor="cross")

    canvas = tk.Canvas(
        root,
        bg="black",
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True)

    def on_mouse_down(event):
        nonlocal start_x, start_y, selection

        start_x = event.x
        start_y = event.y

        selection = canvas.create_rectangle(
            start_x,
            start_y,
            start_x,
            start_y,
            outline="red",
            width=2
        )

    def on_mouse_move(event):
        if selection is not None:
            canvas.coords(
                selection,
                start_x,
                start_y,
                event.x,
                event.y
            )

    def on_mouse_up(event):
        nonlocal result

        x = min(start_x, event.x)
        y = min(start_y, event.y)

        width = abs(event.x - start_x)
        height = abs(event.y - start_y)

        result = (
            screen_width,
            screen_height,
            x,
            y,
            width,
            height
        )

        root.destroy()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

    return result

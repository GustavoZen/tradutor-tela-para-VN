import tkinter as tk

PADDING_X = 8
PADDING_Y = 4


class TranslationOverlay:
    def __init__(self, x, bottom, max_width):
        # bottom: coordenada y onde fica a borda de baixo da janela.
        # A janela cresce para cima a partir dela.
        self.x = x
        self.bottom = bottom

        self.root = tk.Tk()

        # Janela sem bordas, sempre por cima das outras
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(background="black")

        self.label = tk.Label(
            self.root,
            text="Aguardando texto...",
            fg="white",
            bg="black",
            font=("Arial", 14),
            # Desconta o padding para a janela inteira não passar de max_width
            wraplength=max_width - 2 * PADDING_X,
            justify="left"
        )
        self.label.pack(padx=PADDING_X, pady=PADDING_Y)

        # Clique com o botão direito fecha a janela
        self.label.bind("<Button-3>", lambda event: self.root.destroy())

        self.reposition()

    def set_text(self, text):
        self.label.config(text=text)
        self.reposition()

    def reposition(self):
        # Calcula o tamanho que o texto precisa antes de posicionar
        self.root.update_idletasks()

        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()

        # Mantém a borda de baixo fixa; o topo sobe conforme a altura.
        # max(0, ...) impede que a janela saia pelo topo da tela.
        top = max(0, self.bottom - height)

        self.root.geometry(f"{width}x{height}+{self.x}+{top}")

    def run(self, results):
        # O Tkinter só pode ser alterado pela thread principal,
        # então a fila é verificada aqui periodicamente
        def check_results():
            while not results.empty():
                self.set_text(results.get())

            self.root.after(200, check_results)

        check_results()
        self.root.mainloop()

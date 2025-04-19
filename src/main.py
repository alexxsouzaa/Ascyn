import customtkinter as ctk
from tkinter import Tk, filedialog
from tools.image_convert import ascii_img


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs, )

        self.title("Ascyn")
        self.geometry("900x500")
        self._apply_appearance_mode("dark")

        # Frame de seleção de arquivos
        self.frame_file = ctk.CTkFrame(
            master=self,
            width=330,
            height=122,
            fg_color="#343434"
        )
        self.frame_file.place(x=21, y=24)

        self.label_frameFile = ctk.CTkLabel(
            master=self,
            text="Selecione o arquivo",
            font=('Segoe UI', 12),
            fg_color="#343434",
            width=110,
            height=20
        )
        self.label_frameFile.place(x=135, y=79)

        # Frame divisor
        self.frame_diviser = ctk.CTkFrame(
            master=self,
            width=330,
            height=2,
            corner_radius=2
        )
        self.frame_diviser.place(x=21, y=184)

        # ComboBox do padrão de caracteres
        self.label_caracteres = ctk.CTkLabel(
            master=self,
            text="Padrão de caracteres",
            font=('Segoe UI', 12),
        )
        self.label_caracteres.place(x=21, y=210)

        self.comboBox_caracteres = ctk.CTkComboBox(
            master=self,
            width=220,
            values=["#@*:. ",
                    "@%#*+=-:. ",
                    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "]
        )
        self.comboBox_caracteres.place(x=21, y=236)

        # ComboBox do extensão de arquivo
        self.label_extensao = ctk.CTkLabel(
            master=self,
            text="Extensão do arquivo",
            font=('Segoe UI', 12),
        )
        self.label_extensao.place(x=21, y=280)

        self.comboBox_extensao = ctk.CTkComboBox(
            master=self,
            width=220
        )
        self.comboBox_extensao.place(x=21, y=307)

        self.button_salvar = ctk.CTkButton(
            master=self,
            text="Salvar",
            height=32
        )
        self.button_salvar.place(x=21, y=430)

        self.button_cancelar = ctk.CTkButton(
            master=self,
            text="Cancelar",
            height=32,
        )
        self.button_cancelar.place(x=211, y=430)

        # Text Box
        self.textbox = ctk.CTkTextbox(
            master=self,
            width=529,
            height=499,
            corner_radius=0
        )
        self.textbox.place(x=372, y=0)

        self.textbox.insert("0.0", "Olá! Este é um texto dentro do Textbox.")
        self.textbox.configure(state="disabled")

        # Altera o curso do mouse
        def on_enter(event):
            self.frame_file.configure(cursor="hand2")

        # Volta ao cursor padrão ao sair do frame
        def on_leave(event):
             self.frame_file.configure(cursor="")

        # Tornando todos os itens do card clicavel
        # Bind para abrir o explorador de arquivos
        self.frame_file.bind("<Button-1>", lambda event: self.open_file())
        self.label_frameFile.bind("<Button-1>", lambda event: self.open_file())

        self.button_cancelar.bind("<Button-1>", lambda event: self.text_insert())

        self.frame_file.bind("<Enter>", on_enter)
        self.frame_file.bind("<Leave>", on_leave)

        self.label_frameFile.bind("<Enter>", on_enter)
        self.label_frameFile.bind("<Leave>", on_leave)

    # Função para abrir o explorador de arquivos
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.caminho_imagem = file_path
            print("Imagem selecionada:", self.caminho_imagem)
            return self.caminho_imagem

    def text_insert(self):
        if self.caminho_imagem:
            ascii_text = ascii_img(self.caminho_imagem, "#@*:. ")
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", ascii_text)
            self.textbox.configure(state="disabled")
        else:
            print("Nenhuma imagem selecionada.")
        

Main = App()
Main.mainloop()
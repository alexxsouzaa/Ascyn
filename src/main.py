import customtkinter as ctk
from tkinter import Tk, filedialog
from tools.image_convert import ascii_img


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs, )

        # Variaveis
        self.caminho_imagem = None

        self.title("Ascyn - ASCII Art")
        self.geometry("900x500+230+100")
        self._apply_appearance_mode("dark")
        self.resizable(False, False)

        # Frame de seleção de arquivos
        self.frame_file = ctk.CTkFrame(
            master=self,
            width=330,
            height=122,
            fg_color="#343434"
        )
        self.frame_file.place(x=21, y=24)

        self.label_frameFile = ctk.CTkLabel(
            master=self.frame_file,
            text="Selecionar arquivo",
            font=('Segoe UI', 12),
            fg_color="#343434",
            width=110,
            height=20
        )
        self.label_frameFile.place(x=110, y=52)

        # Entry do caminho do arquivo
        self.entry_pathFile = ctk.CTkEntry(
            master=self,
            fg_color="#343434",
            width=330,
            height=32,
            border_width=0
            
        )
        self.entry_pathFile.place(x=21, y=158)
        self.entry_pathFile.configure(state="disabled")

        # Frame divisor
        self.frame_diviser = ctk.CTkFrame(
            master=self,
            width=330,
            height=2,
            corner_radius=2
        )
        self.frame_diviser.place(x=21, y=208)

        # ComboBox do padrão de caracteres
        self.label_caracteres = ctk.CTkLabel(
            master=self,
            text="Padrão de caracteres",
            font=('Segoe UI', 12),
        )
        self.label_caracteres.place(x=21, y=226)

        self.comboBox_caracteres = ctk.CTkComboBox(
            master=self,
            width=220,
            values=["@#*:. ",
                    "@%#0*=-:. ",
                    "@%#0B$&*+=-:,. "],
            state="readonly"
        )
        self.comboBox_caracteres.place(x=21, y=252)
        self.comboBox_caracteres.set("@#*:. ")

        # ComboBox do extensão de arquivo
        self.label_extensao = ctk.CTkLabel(
            master=self,
            text="Extensão do arquivo",
            font=('Segoe UI', 12),
        )
        self.label_extensao.place(x=21, y=292)

        self.comboBox_extensao = ctk.CTkComboBox(
            master=self,
            width=220,
            values=[
                ".txt",
                ".asc"
            ]
        )
        self.comboBox_extensao.place(x=21, y=318)
        self.comboBox_extensao.set(".txt")

        # Inverte cores
        self.switch_inverteCores = ctk.CTkSwitch(
            master=self,
            text="Inverte cores?",
            onvalue="True",
            offvalue="False"
        )
        self.switch_inverteCores.place(x=21, y=360)

        self.button_converte = ctk.CTkButton(
            master=self,
            text="Converte",
            height=32,
            command=self.text_insert
        )
        self.button_converte.place(x=21, y=430)
        #self.button_converte.configure(state="disabled")

        self.button_salvar = ctk.CTkButton(
            master=self,
            text="Salvar",
            text_color="#ffffff",
            height=32,
            fg_color="#343434",
            hover_color="#444444",
            border_color="#ffffff",
            border_width=1,
            command=self.save_file
        )
        self.button_salvar.place(x=211, y=430)
        #self.button_salvar.configure(state="disabled")

        # Text Box
        self.textbox = ctk.CTkTextbox(
            master=self,
            width=529,
            height=499,
            corner_radius=0,
            font=("Courier New", 12)
        )
        self.textbox.place(x=372, y=0)
        self.textbox.configure(state="disabled", wrap="none")

        self.frame_feedback = ctk.CTkFrame(
            master=self,
            width=290,
            height=40,
            fg_color="#2EB342",
            bg_color="#343434",
            corner_radius=8
        )
        self.frame_feedback.place(x=41, y=-50)
        
        self.label_feedback = ctk.CTkLabel(
            master=self.frame_feedback,
            text="Imagem convertida com sucesso!"
        )
        self.label_feedback.place(x=50, y=7)

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

        self.frame_file.bind("<Enter>", on_enter)
        self.frame_file.bind("<Leave>", on_leave)

        self.label_frameFile.bind("<Enter>", on_enter)
        self.label_frameFile.bind("<Leave>", on_leave)

    # Função para abrir o explorador de arquivos
    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Selecione uma imagem",
                filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if file_path:
                self.caminho_imagem = file_path
                self.entry_pathFile.configure(state="normal")
                self.entry_pathFile.delete(0, 'end')
                self.entry_pathFile.insert(0, self.caminho_imagem)
                self.entry_pathFile.configure(state="disabled")
                self.button_converte.configure(state="normal")
                self.button_salvar.configure(state="normal")
                return self.caminho_imagem
        except Exception as error:
            self.show_feedback("Erro ao selecionar a imagem", "#FE696B", "#000000") # Aviso que nenhuma imagem foi selecionada
            print("Erro ao selecionar a imagem: ", error)

    def text_insert(self):
        try:
            if self.caminho_imagem:
                ascii_text = ascii_img(self.caminho_imagem, self.comboBox_caracteres.get(), self.switch_inverteCores.get()) # Converte a imagem em Asciis
                self.textbox.configure(state="normal")  # Ativa a edição de texto do TextBox
                self.textbox.delete("0.0", "end")   # Apaga o texto do TextBox
                self.textbox.insert("0.0", ascii_text) # Insere o texto Ascci no TextBox
                self.textbox.configure(state="disabled") # Desabilitar a edição de texto do TextBox
                self.show_feedback("Imagem convertida com sucesso!", "#69FE69", "#000000") # Aviso que a imagem foi convertida com sucesso
            else:
                self.show_feedback("Nenhuma imagem selecionada.", "#FE696B", "#000000") # Aviso que nenhuma imagem foi selecionada
                print("Nenhuma imagem selecionada.")
        except Exception as error:
                self.show_feedback("Erro ao converter imagem", "#FE696B", "#000000") # Aviso que nenhuma imagem foi selecionada
                print("Erro ao converte imagem: ", error)
    
    def save_file(self):
        try:
            conteudo = self.textbox.get("0.0", "end").strip()
            if conteudo:
                extensao = self.comboBox_extensao.get()
                tipos_arquivo = [("Arquivo ASCII", f"*{extensao}")]

                file_path = filedialog.asksaveasfilename(
                    defaultextension=extensao,
                    filetypes=tipos_arquivo,
                )

                if file_path:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(conteudo)
                        self.show_feedback("Arquivo salvo com sucesso!", "#ffffff", "#000000")
                        print(f"Arquivo salvo com sucesso em {file_path}")
                else:
                    print("Salvamento cancelado")
            else:
                print("O arquivo não foi convertido")

        except Exception as error:
            self.show_feedback("Erro ao salvar o arquivo!", "#FE696B", "#ffffff")
            print("Erro ao salvar o arquivo: ", error)

    def show_feedback(self, mensagem=str, color=str, txt_color=str):
        self.label_feedback.configure(text=mensagem, text_color=txt_color)
        self.frame_feedback.configure(fg_color=color)

        # Centraliza o texto dinamicamente no frame de feedback
        self.label_feedback.update_idletasks()
        label_width = self.label_feedback.winfo_reqwidth()
        frame_width = self.frame_feedback.winfo_width()
        centered_x = (frame_width - label_width) // 2
        self.label_feedback.place(x=centered_x, y=7)

        self.frame_feedback.place(x=41, y=-50)
        self.slide_feedback(y_inicial=-50, y_final=16, subindo=False)

    def slide_feedback(self, y_inicial, y_final, subindo=False, passo=2, delay=10):
        if not subindo and y_inicial < y_final:
            y_inicial += passo
            self.frame_feedback.place(x=41, y=y_inicial)
            self.after(delay, lambda: self.slide_feedback(y_inicial, y_final, subindo, passo, delay))
        elif not subindo:
            # Espera 2 segundos, depois anima pra cima
            self.after(2000, lambda: self.slide_feedback(y_inicial=y_final, y_final=-50, subindo=True, passo=2, delay=10))
        elif subindo and y_inicial > y_final:
            y_inicial -= passo
            self.frame_feedback.place(x=41, y=y_inicial)
            self.after(delay, lambda: self.slide_feedback(y_inicial, y_final, subindo, passo, delay))
        else:
            self.frame_feedback.place_forget()



Main = App()
Main.mainloop()
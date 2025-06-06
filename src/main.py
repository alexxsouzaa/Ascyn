import customtkinter as ctk
from tkinter import Tk, filedialog
from tools.image_convert import ascii_img
from PIL import Image, ImageTk
from io import BytesIO
import base64


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs, )

        # Variaveis
        self.caminho_imagem = None

        self.title("Ascyn - ASCII Art")
        self.geometry("900x500+230+100")
        self.overrideredirect(False)
        self._apply_appearance_mode("dark")
        self.resizable(False, False)

        # Ícone da janela (em base64)
        icon_data = ("""iVBORw0KGgoAAAANSUhEUgAAABUAAAAVCAYAAACpF6WWAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAFoSURBVHgBtVW7cYQwEN05R5fRwdEBlEAHlGAInakDKIES6MB0AB1A6ExQAZCRyfs0IGMPkvHdeWeeZiUNb99+AKIv8xiC8c6QjJGhHMB9y6gZCR2YvxKpByBXHmOPEu6JkbGWrp4IceHllRzm+z7VdU3jOJJSitq2pTAMXY9EWFpbVCZUUkolhFCe5+mzPM8VBzB7SwnsXS7LUpP8PAcpq3VNxTEhlMCgFvsoilSSJHq/P7fg+AIkXD/jQx1UF0WhScndrOML1LFpGu1XVaX38KF2C2bDhRxd77pO+7fbzfg4H4aBXGYlDYKA+r7XPkZomibjbwH+TMqNMg+DkOtKnDrFcXw/KRRtStM0NQMP/zdS2OGcotvoOp17Nb/N6Qsvb7R+BPZ2vV4pyzKa51nvl2XROGEfWCpbVIwPp6q4DNo/qbQBqbgjRRcSWlOXTyKU+zr49A9f/s2StSaYmTP/qH7tiaBdsz8BR3uR6SFJ2xsAAAAASUVORK5CYII=""")

        image_stream = BytesIO(base64.b64decode(icon_data))
        icon_image = Image.open(image_stream)
        tk_icon = ImageTk.PhotoImage(icon_image)
        self.iconphoto(False, tk_icon)


        # Frame de seleção de arquivos
        self.frame_file = ctk.CTkFrame(
            master=self,
            width=340,
            height=122,
            fg_color="#343434"
        )
        self.frame_file.place(x=16, y=16)

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
        self.label_pathFile = ctk.CTkLabel(
             master=self,
             text="Caminho da imagem:"
         )
        self.label_pathFile.place(x=16, y=142)

        self.entry_pathFile = ctk.CTkEntry(
            master=self,
            fg_color="#343434",
            width=340,
            height=32,
            border_width=0
            
        )
        self.entry_pathFile.place(x=16, y=169)
        self.entry_pathFile.configure(state="disabled")

        # Frame divisor
        self.frame_diviser = ctk.CTkFrame(
            master=self,
            width=340,
            height=2,
            corner_radius=2
        )
        self.frame_diviser.place(x=16, y=216)

        # ComboBox do padrão de caracteres
        self.label_caracteres = ctk.CTkLabel(
            master=self,
            text="Padrão de caracteres:",
            font=('Segoe UI', 12),
        )
        self.label_caracteres.place(x=16, y=226)

        self.comboBox_caracteres = ctk.CTkComboBox(
            master=self,
            width=220,
            values=["@#*:. ",
                    "@%#0*=-:. ",
                    "@%#0B$&*+=-:,. "],
            state="readonly",
            fg_color="#343434",
            border_color="#343434"
        )
        self.comboBox_caracteres.place(x=16, y=252)
        self.comboBox_caracteres.set("@#*:. ")

        # ComboBox do extensão de arquivo
        self.label_extensao = ctk.CTkLabel(
            master=self,
            text="Extensão do arquivo:",
            font=('Segoe UI', 12),
        )
        self.label_extensao.place(x=16, y=292)

        self.comboBox_extensao = ctk.CTkComboBox(
            master=self,
            width=220,
            values=[
                ".txt",
                ".asc"
            ],
            state="readonly",
            fg_color="#343434",
            border_color="#343434"
        )
        self.comboBox_extensao.place(x=16, y=318)
        self.comboBox_extensao.set(".txt")

        # Inverte cores
        self.switch_inverteCores = ctk.CTkSwitch(
            master=self,
            text="Inverte cores?",
            onvalue="True",
            offvalue="False"
        )
        self.switch_inverteCores.place(x=16, y=360)

        self.button_converte = ctk.CTkButton(
            master=self,
            text="Converte",
            height=32,
            width=100,
            font=('Segoe UI', 12),
            command=self.text_insert
        )
        self.button_converte.place(x=16, y=437)
        #self.button_converte.configure(state="disabled")

        self.button_copy = ctk.CTkButton(
            master=self,
            text="Copiar",
            font=('Segoe UI', 12),
            height=32,
            width=100,
            fg_color="#ffffff",
            hover_color="#C7C7C7",
            text_color="#000000",
            command=self.copy_text
        )
        self.button_copy.place(x=136, y=437)
        self.button_copy.configure(state="disabled")

        self.button_salvar = ctk.CTkButton(
            master=self,
            text="Salvar",
            text_color="#ffffff",
            font=('Segoe UI', 12),
            height=32,
            width=100,
            fg_color="#343434",
            hover_color="#444444",
            border_color="#ffffff",
            border_width=1,
            command=self.save_file
        )
        self.button_salvar.place(x=256, y=437)
        self.button_salvar.configure(state="disabled")

        # Text Box
        self.textbox = ctk.CTkTextbox(
            master=self,
            width=529,
            height=499,
            corner_radius=0,
            font=("Courier New", 12)
        )
        self.textbox.place(x=372, y=0)
        self.text_demo()

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
                self.button_salvar.configure(state="normal")  # Habilita salvar só se algo foi gerado
                self.button_copy.configure(state="normal") # Habilita copia o texto do TextBox
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
                self.show_feedback("O arquivo não foi convertido", "#FE696B", "#000000")
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
            # Espera 1,2 segundos, depois anima pra cima
            self.after(1200, lambda: self.slide_feedback(y_inicial=y_final, y_final=-50, subindo=True, passo=2, delay=10))
        elif subindo and y_inicial > y_final:
            y_inicial -= passo
            self.frame_feedback.place(x=41, y=y_inicial)
            self.after(delay, lambda: self.slide_feedback(y_inicial, y_final, subindo, passo, delay))
        else:
            self.frame_feedback.place_forget()

    def copy_text(self):
        try:
            content = self.textbox.get("0.0", "end").strip()
            if content:
                self.clipboard_clear()
                self.clipboard_append(content)
                self.show_feedback("Texto copiado com sucesso!", "#5D96FF", "#000000")
            else:
                self.show_feedback("Nenhum conteúdo para copiar.", "#FE696B", "#000000")
        except:
            self.show_feedback("Erro ao copiar o texto!", "#FE696B", "#ffffff")

    def text_demo(self):
        self.textbox.configure(state="normal")  # Ativa a edição de texto do TextBox
        self.textbox.delete("0.0", "end")   # Apaga o texto do TextBox
        self.textbox.insert("0.0", """
                            



                            
                                    .....::::::...                               
                                 .:##@@@@@@@@@@##*:.                            
                             .:*###**::......:**####*:                          
                           ..:*###*..          .:#@@@*.                         
                          .*##**:.              .:#@@*.                         
                         .*#@@*:        ...:..  .*@@@*.                         
                         .*#@#*.     .:*#***::::*#@@@*.                         
                       ..:*##*:    .:*#@@#*::::**#@@#:                          
                       .:**##*:   :*##**:.    .:*###*:                          
                      .::**#*:.  .:###*:.     .:**##*:                          
                      .:*****:.  .*#@#*.     .:**##*:.                          
                      .*###*:.   .*@@@*.     .*###*::.                          
                      .*##*:..   .*@@@*:....:*@@@#*:.                           
                      :#@@*:.     :*##***::::*###*:.                            
                      :#@@#:       ..::***::......                              
                      :#@@#:.                                                   
                      .*####**:..                                               
                       .::*####**::::...                                        
                           .:**##@@@@#*:..                                      
                              .........""") # Insere o texto Ascci no TextBox
        self.textbox.configure(state="disabled", wrap="none")


Main = App()
Main.mainloop()
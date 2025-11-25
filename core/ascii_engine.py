# core/ascii_engine.py
from PIL import Image, ImageEnhance, ImageOps
from typing import Optional

class AsciiEngine:
    CHARS = "@%#*+=-:. "[::-1]  # do mais escuro pro mais claro

    def __init__(self):
        self.imagem_original: Optional[Image.Image] = None
        self.imagem_processada: Optional[Image.Image] = None

        # Ajustes
        self.brilho = 1.0
        self.contraste = 1.0
        self.saturacao = 1.0
        self.inverter = False

    def carregar_imagem(self, caminho: str) -> bool:
        try:
            self.imagem_original = Image.open(caminho).convert("RGB")
            self.imagem_processada = self.imagem_original.copy()
            return True
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            return False

    def set_ajuste(self, tipo: str, valor):
        if tipo == "brilho":
            self.brilho = valor
        elif tipo == "contraste":
            self.contraste = valor
        elif tipo == "saturacao":
            self.saturacao = valor
        elif tipo == "inverter":
            self.inverter = bool(valor)

        # RECALCULA A IMAGEM COM OS NOVOS AJUSTES
        self._aplicar_ajustes()

    def _aplicar_ajustes(self):
        """Aplica TODOS os ajustes na imagem original e salva em processada"""
        if not self.imagem_original:
            return

        img = self.imagem_original.copy()

        # Inverte se necessário
        if self.inverter:
            img = ImageOps.invert(img.convert("L")).convert("RGB")

        # Aplica os 3 ajustes principais
        img = ImageEnhance.Brightness(img).enhance(self.brilho)
        img = ImageEnhance.Contrast(img).enhance(self.contraste)
        img = ImageEnhance.Color(img).enhance(self.saturacao)

        # SALVA A IMAGEM JÁ AJUSTADA
        self.imagem_processada = img

    def converter_imagem(self, largura: int = 140) -> str:
        if not self.imagem_processada:
            return "Nenhuma imagem carregada"

        # USA A IMAGEM JÁ COM AJUSTES APLICADOS
        img_cinza = self.imagem_processada.convert("L")

        # Mantém proporção
        ratio = img_cinza.height / img_cinza.width
        altura = int(largura * ratio * 0.55)

        img_cinza = img_cinza.resize((largura, altura), Image.Resampling.LANCZOS)
        pixels = img_cinza.getdata()

        ascii_str = "".join(self.CHARS[pixel * (len(self.CHARS)-1) // 255] for pixel in pixels)
        return "\n".join(ascii_str[i:i+largura] for i in range(0, len(ascii_str), largura))

    def reset(self):
        self.brilho = self.contraste = self.saturacao = 1.0
        self.inverter = False
        if self.imagem_original:
            self.imagem_processada = self.imagem_original.copy()
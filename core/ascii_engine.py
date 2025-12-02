# core/ascii_engine.py
from PIL import Image, ImageEnhance, ImageOps
from typing import Optional, Dict
from PySide6.QtWidgets import QSlider

class AsciiEngine:
    """Engine responsável por carregar imagem, aplicar ajustes e gerar ASCII art."""
    
    def __init__(self):
        self.original_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None

        # Ajustes padrão
        self.adjustments: Dict[str, float | bool] = {
            "brightness": 1.0,
            "contrast": 1.0,
            "saturation": 1.0,
            "invert": False,
        }
        
    # =====================================================================
    # CARREGAMENTO
    # =====================================================================
    def load_image(self, path: str) -> bool:
        """Carrega uma imagem do disco e copia para processamento."""
        
        try:
            self.original_image = Image.open(path).convert("RGB")
            self.processed_image = self.original_image.copy()
            return True
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            return False

    # =====================================================================
    # AJUSTES
    # =====================================================================
    def set_adjustment(self, key: str, value):
        """Atualiza um ajuste específico e recalcula a imagem processada."""

        if key not in self.adjustments:
            print(f'Ajuste inválido: {key}')
            return
        
        self.adjustments[key] = value
        # Aplica os ajustes na imagem
        self._apply_adjustments()

    def _apply_adjustments(self):
        """Aplica todos os ajustes sobre a imagem original."""
        if not self.original_image:
            return

        img = self.original_image.copy()

        # Inversão de cores
        if self.adjustments["invert"]:
            img = ImageOps.invert(img.convert("L")).convert("RGB")

        # Aplica os 3 ajustes principais
        img = ImageEnhance.Brightness(img).enhance(self.adjustments["brightness"])
        img = ImageEnhance.Contrast(img).enhance(self.adjustments["contrast"])
        img = ImageEnhance.Color(img).enhance(self.adjustments["saturation"])

        # Salva a imagem já ajustada
        self.processed_image = img

    # =====================================================================
    # ASCII ART
    # =====================================================================
    def to_ascii(
        self,
        charset: str="@%#*+=-:. ",
        width: QSlider = 120
        ) -> str:
        
        """Converte a imagem processada para ASCII Art."""
        
        if not self.processed_image:
            return "Nenhuma imagem carregada"

        # Converte a imagem para escala de cinza
        img_gray = self.processed_image.convert("L")
        
        # Calcula height mantendo proporção
        ratio = img_gray.height / img_gray.width
        height = int(width * ratio * 0.55)

        # Ajusta charset
        charset = charset[::-1]
        
        # Redimensiona
        img_gray = img_gray.resize((width, height), Image.Resampling.LANCZOS)
        pixels = img_gray.getdata()

        # Constrói ASCII
        scale = len(charset) - 1
        ascii_pixels  = "".join(charset[pixel * scale // 255] for pixel in pixels)
        return "\n".join(ascii_pixels[i:i+width] for i in range(0, len(ascii_pixels), width))

    # =====================================================================
    # RESET
    # =====================================================================
    def reset(self):
        """Restaura ajustes e imagem processada ao estado original."""
        
        self.adjustments.update({
            "brightness": 1.0,
            "contrast": 1.0,
            "saturation": 1.0,
            "invert": False,
        })
        
        if self.original_image:
            self.processed_image = self.original_image.copy()
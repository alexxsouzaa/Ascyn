from PIL import Image, ImageOps

def converter_imagem(
    caminho_imagem,
    caracteres,
    inverter,
    largura: int = 100,
    altura: int = 40
    
    ):
    # Caminho da imagem
    img = Image.open(caminho_imagem).convert('L')

     # Inverter tons de cinza se necessário
    if inverter == "True":
        img = ImageOps.invert(img)

    # Redimensiona mantendo proporção
    img = img.resize((largura, altura), Image.Resampling.LANCZOS)
    # Caracteres
    ascii_chars = caracteres

    pixels = img.getdata()
    ascii_str = "".join([ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels])

    width = img.width
    img_text = "\n".join([ascii_str[i:i+width] for i in range(0, len(ascii_str), width)])

    return img_text
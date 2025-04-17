from PIL import Image
import os

img_path = os.path

img = Image.open("assets\\logo2.png").convert('L')
img = img.resize((100, 50))

ascii_chars = ascii_chars = "@$%+-. "

pixels = img.getdata()
ascii_str = "".join([ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels])

width = img.width
ascii_img = "\n".join([ascii_str[i:i+width] for i in range(0, len(ascii_str), width)])

print(ascii_img)

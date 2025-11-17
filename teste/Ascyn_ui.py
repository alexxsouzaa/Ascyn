import os
import sys
from PySide6.QtCore import QResource, QFile
from PySide6.QtGui import QIcon

# === 1. CAMINHO ABSOLUTO ===
rcc_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "ascyn_resource_icons.rcc")
print(f"Procurando .rcc em: {rcc_path}")

if not os.path.exists(rcc_path):
    print("ERRO: .rcc não encontrado!")
    sys.exit(1)

# === 2. REGISTRA ===
if QResource.registerResource(rcc_path):
    print("SUCESSO: .rcc carregado!")
else:
    print("FALHA: QResource.registerResource() retornou False")
    sys.exit(1)

# === 3. TESTE DE ARQUIVO ===
for name in ["close.svg", "maximize.svg", "minimize.svg"]:
    resource_path = f":/icons/{name}"
    if QFile.exists(resource_path):
        print(f"{name} → ENCONTRADO!")
    else:
        print(f"{name} → NÃO ENCONTRADO!")
        print(f"   Verifique: pasta, nome, case-sensitive, .rcc gerado")
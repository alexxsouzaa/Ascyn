
# Ascyn - ASCII Art Converter

**Ascyn** é um aplicativo simples que converte imagens em arte ASCII. Ele permite selecionar uma imagem, escolher o padrão de caracteres para a conversão e exportar o resultado como um arquivo de texto. O programa também oferece funcionalidades para copiar o texto gerado e salvar o arquivo ASCII em diferentes extensões.

## Funcionalidades

- **Seleção de Imagem**: Selecione uma imagem no formato PNG, JPG, JPEG, BMP ou GIF.
- **Conversão para ASCII**: Converta a imagem selecionada em arte ASCII usando diferentes padrões de caracteres.
- **Inversão de Cores**: Opção para inverter as cores da imagem na arte ASCII.
- **Exportação de Arquivo**: Salve a arte ASCII em um arquivo `.txt` ou `.asc`.
- **Copiar para Área de Transferência**: Copie a arte ASCII gerada para a área de transferência.

## Requisitos

O projeto foi desenvolvido utilizando as seguintes dependências:

- **Python 3.x**
- **CustomTkinter** - Biblioteca para criar interfaces gráficas modernas com Tkinter.
- **Pillow** - Biblioteca para manipulação de imagens.
- **base64** - Para carregar o ícone da aplicação em formato base64.

## Dependências

Para instalar as dependências necessárias, execute o seguinte comando no terminal:

```bash
pip install customtkinter pillow
```

## Como Usar

1. Clone ou baixe o repositório.
2. Instale as dependências:
    ```bash
    pip install customtkinter pillow
    ```
3. Execute o script principal:
    ```bash
    python main.py
    ```
4. Utilize a interface para:
    - Selecionar uma imagem.
    - Escolher o padrão de caracteres para a conversão.
    - Inverter as cores (se necessário).
    - Converter a imagem para arte ASCII.
    - Copiar ou salvar o arquivo gerado.

## Licença

Este projeto está licenciado sob a [Licença GPL-3.0](https://opensource.org/licenses/GPL-3.0).

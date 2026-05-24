# OggToMp3 Converter GUI (v1.0.0)

A modern, simple, and efficient audio converter developed in Python to transform `.ogg` files into `.mp3` with automatic sequential organization and native high-fidelity conversion.

## 🚀 Features

- **Native Conversion (No FFmpeg required):** Uses professional audio libraries (`soundfile` & `lameenc`) for high-fidelity conversion, bypassing metadata issues found in WhatsApp voice notes.
- **Bilingual Support (EN/PT):** Integrated language selector in the GUI to switch between English and Portuguese instantly.
- **Intuitive Graphical Interface:** Single-list layout with full paths and sequential numbering for total control before conversion.
- **Multiple Selection:** Add as many `.ogg` files as you want at once.
- **Smart Sorting:** Organize your files by **Name** (alphabetical order) or **Date** (modification date).
- **Sequential Renaming (Leading Zeros):** Output files are automatically renamed in numbered format (e.g., `01.mp3`, `02.mp3`).
- **Background Processing (Threading):** Conversion doesn't freeze the interface.

## 🛠️ Prerequisites

To use this program, you will need:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **Dependencies**:
    ```bash
    pip install soundfile lameenc numpy
    ```

## 📦 Installation and Usage

1.  Clone this repository or download the files.
2.  Install the required dependencies: `pip install soundfile lameenc numpy`
3.  Run the program:
    ```bash
    python converter_gui.py
    ```

## 🛠️ Generating an Executable (.exe) for Windows

To generate a standalone executable for Windows:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Generate the executable:**
    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --name "Ogg2Mp3Converter" converter_gui.py
    ```

---

# OggToMp3 Converter GUI (v1.0.0 - Português)

Um conversor de áudio moderno, simples e eficiente, desenvolvido em Python para transformar arquivos `.ogg` em `.mp3` com organização sequencial automática e conversão nativa de alta fidelidade.

## 🚀 Funcionalidades

- **Conversão Nativa (Sem necessidade de FFmpeg):** Utiliza bibliotecas profissionais (`soundfile` e `lameenc`) para garantir a integridade do áudio, resolvendo problemas de truncamento em arquivos do WhatsApp.
- **Suporte Bilíngue (EN/PT):** Seletor de idioma integrado na interface para alternar entre Inglês e Português instantaneamente.
- **Interface Gráfica Intuitiva:** Layout de lista única com caminhos completos e numeração sequencial.
- **Seleção Múltipla:** Adicione quantos arquivos `.ogg` desejar de uma só vez.
- **Ordenação Inteligente:** Organize seus arquivos por **Nome** ou por **Data**.
- **Processamento em Background:** A conversão não trava a interface.

## 🛠️ Pré-requisitos

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **Dependências**:
    ```bash
    pip install soundfile lameenc numpy
    ```

## 📦 Instalação e Uso

1.  Baixe os arquivos do projeto.
2.  Instale as dependências: `pip install soundfile lameenc numpy`
3.  Execute:
    ```bash
    python converter_gui.py
    ```

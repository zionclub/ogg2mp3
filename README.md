# OggToMp3 Converter GUI

A modern, simple, and efficient audio converter developed in Python to transform `.ogg` files into `.mp3` with automatic sequential organization.

## 🚀 Features

- **Intuitive Graphical Interface:** Single-list layout with full paths and sequential numbering for total control before conversion.
- **Native Conversion:** Uses professional audio libraries (`soundfile` & `lameenc`) for high-fidelity conversion, bypassing FFmpeg's metadata issues.
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

If you want to turn this script into an executable file that runs without the need to install Python on other Windows machines, follow these steps:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Generate the executable:**
    Run the command below in the project folder:
    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --name "Ogg2Mp3Converter" converter_gui.py
    ```

    *Tip: If the `python` command doesn't work, try `python3` or just `pyinstaller` directly.*

    - `--onefile`: Packages everything into a single `.exe` file.
    - `--windowed`: Prevents a black terminal window from appearing when opening the program.
    - `--name`: Sets the final file name.

3.  **Locate the file:**
    After finishing, the executable will be inside the `dist/` folder.

*Note: The end user will still need to have **FFmpeg** installed on the system or the `ffmpeg.exe` must be in the same folder as the generated executable.*

## 📖 How to Use

1.  **Select Files:** Click the top-left button and select the `.ogg` files you want to convert.
2.  **Output Directory:** Click the top-right button to choose where the `.mp3` files will be saved.
3.  **Sort:** Choose between sorting by Name or Date in the bottom panel. The list will be updated instantly.
4.  **Convert:** Click "Convert" and follow the progress bar and logs.

## 💻 Technical Architecture

- **Language:** Python
- **GUI:** `tkinter` & `ttk` (Native to Python, no need for heavy extra packages).
- **Conversion:** Direct calls to `FFmpeg` via `subprocess` module for maximum performance and audio fidelity.
- **Concurrency:** `threading` module to keep the UI responsive during audio processing.

---

# OggToMp3 Converter GUI (Português)

Um conversor de áudio moderno, simples e eficiente, desenvolvido em Python para transformar arquivos `.ogg` em `.mp3` com organização sequencial automática.

## 🚀 Funcionalidades

- **Interface Gráfica Intuitiva:** Layout de lista única com caminhos completos e numeração sequencial para total controle antes da conversão.
- **Seleção Múltipla:** Adicione quantos arquivos `.ogg` desejar de uma só vez.
- **Ordenação Inteligente:** Organize seus arquivos por **Nome** (ordem alfabética) ou por **Data** (data de modificação).
- **Renomeação Sequencial (Leading Zeros):** Os arquivos de saída são renomeados automaticamente de forma numerada (ex: `01.mp3`, `02.mp3`). O programa calcula automaticamente a quantidade de zeros à esquerda com base no volume total de arquivos (ex: se forem 100 arquivos, começará em `001.mp3`).
- **Processamento em Background (Threading):** A conversão não trava a interface. Você pode acompanhar o progresso em tempo real através da barra de progresso e logs detalhados.
- **Verificação de Dependências:** Alerta automático caso o FFmpeg não seja detectado no sistema.

## 🛠️ Pré-requisitos

Para utilizar este programa, você precisará de:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **FFmpeg**: O motor de conversão utilizado por este programa.
    - **Windows:**
        - **Via CLI (Recomendado):**
          ```powershell
          # Usando Winget (Nativo do Windows 10/11)
          winget install ffmpeg
          
          # Usando Chocolatey
          choco install ffmpeg
          ```
        - **Manual:** Baixe em [ffmpeg.org](https://ffmpeg.org/download.html), extraia e adicione a pasta `bin` ao seu PATH do sistema.
    - **Linux (Ubuntu/Debian):** `sudo apt install ffmpeg`
    - **macOS:** `brew install ffmpeg`

## 📦 Instalação e Uso

1.  Clone este repositório ou baixe os arquivos.
2.  Abra o terminal na pasta do projeto.
3.  Execute o programa:
    ```bash
    python converter_gui.py
    ```

## 🛠️ Gerando um Executável (.exe) para Windows

Se você deseja transformar este script em um arquivo executável que rode sem a necessidade de instalar o Python em outras máquinas Windows, siga estes passos:

1.  **Instale o PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Gere o executável:**
    Execute o comando abaixo na pasta do projeto:
    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --name "Ogg2Mp3Converter" converter_gui.py
    ```

    *Dica: Se o comando `python` não funcionar, tente `python3` ou apenas `pyinstaller` diretamente.*

    - `--onefile`: Empacota tudo em um único arquivo `.exe`.
    - `--windowed`: Impede que uma janela de terminal preta apareça ao abrir o programa.
    - `--name`: Define o nome do arquivo final.

3.  **Localize o arquivo:**
    Após o término, o executável estará dentro da pasta `dist/`.

*Nota: O usuário final ainda precisará ter o **FFmpeg** instalado no sistema ou o `ffmpeg.exe` deve estar na mesma pasta do executável gerado.*

## 📖 Como Usar

1.  **Selecionar Arquivos:** Clique no botão superior esquerdo e selecione os arquivos `.ogg` que deseja converter.
2.  **Diretório de Saída:** Clique no botão superior direito para escolher onde os arquivos `.mp3` serão salvos.
3.  **Ordenar:** Escolha entre ordenar por Nome ou Data no painel inferior. A lista será atualizada instantaneamente.
4.  **Converter:** Clique em "Converter" e acompanhe a barra de progresso e os logs.

## 💻 Arquitetura Técnica

- **Linguagem:** Python
- **GUI:** `tkinter` & `ttk` (Nativo do Python, sem necessidade de pacotes extras pesados).
- **Conversão:** Chamadas diretas ao `FFmpeg` via módulo `subprocess` para máxima performance e fidelidade de áudio.
- **Concorrência:** Módulo `threading` para manter a UI responsiva durante o processamento de áudio.

---
Desenvolvido para ser simples, rápido e direto ao ponto.

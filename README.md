# Tradutor de Tela para VN's

Ferramenta que lê o texto de uma área da tela com OCR, traduz e mostra a tradução numa janela sobreposta, atualizando sozinha sempre que o texto muda.

## Objetivo

Este é um projeto de **estudo**. A meta de longo prazo é chegar a um software capaz de traduzir  **qualquer Visual Novel** enquanto ela é jogada, sem depender de patches de tradução ou de ferramentas específicas de cada engine.

Etapas:

- [x] Selecionar uma área da tela
- [x] Capturar a imagem dessa área
- [x] Ler o texto da imagem (OCR)
- [x] Traduzir o texto
- [x] Captura contínua, traduzindo só quando o texto muda
- [x] Janela sobreposta exibindo a tradução
- [ ] Suporte a japonês (OCR e tradução)
- [ ] Atalhos de teclado (pausar, reselecionar a área)
- [ ] Gerar executável para outras pessoas usarem

## Como funciona

```
Selecionar área ──► Capturar imagem ──► OCR ──► Texto mudou? ──► Traduzir ──► Exibir
                          ▲                          │ não
                          └──── espera 1 segundo ◄───┘
```

1. Uma tela escura cobre o monitor e você arrasta o mouse para marcar a área com o texto (a caixa de diálogo da VN, por exemplo).
2. Uma thread em segundo plano captura essa área a cada segundo e passa a imagem pelo Tesseract.
3. Se o texto lido for diferente do anterior, ele é enviado ao tradutor.
4. A tradução aparece numa janela preta logo **acima** da área, que cresce para cima conforme o tamanho do texto.

Para fechar, clique com o **botão direito** na janela de tradução.

## Requisitos

### Softwares

| Software | Para quê | Observação |
|---|---|---|
| [Python 3.10+](https://www.python.org/downloads/) | Rodar o projeto | No Windows, marque "Add Python to PATH" na instalação |
| [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) | Reconhecer o texto nas imagens | Programa externo, **não** é instalado pelo `pip` |
| Conexão com a internet | Tradução | A tradução é feita por um serviço online |

### Bibliotecas Python

| Biblioteca | Para quê |
|---|---|
| `tkinter` | Seleção da área e janela de tradução (já vem com o Python no Windows) |
| `mss` | Captura rápida de uma região da tela |
| `Pillow` | Manipulação das imagens capturadas |
| `pytesseract` | Ponte entre o Python e o Tesseract |
| `deep-translator` | Acesso a serviços de tradução (MyMemory, Google, etc.) |

## Instalação

### 1. Tesseract

**Windows**: baixe e execute o instalador do [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), ou use:

```powershell
winget install UB-Mannheim.TesseractOCR
```

O instalador **não** adiciona o Tesseract ao PATH. Adicione manualmente:

```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Program Files\Tesseract-OCR", "User")
```

Feche e abra o terminal e confira com `tesseract --version`.

**Linux (Debian/Ubuntu)**:

```bash
sudo apt install tesseract-ocr tesseract-ocr-eng python3-tk
```

### 2. Dependências Python

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

Selecione a área com o texto e deixe a janela de tradução aberta enquanto lê.

Os idiomas são definidos em `main.py`:

```python
reader = TesseractReader(lang="eng")                                     # idioma do OCR
translator = MyMemoryTranslatorAdapter(source="en-US", target="pt-BR")  # origem → destino
```

## Estrutura do projeto

```
├── main.py                  # Junta as etapas e roda o laço contínuo
├── screen/
│   ├── selector.py          # Seleção da área com o mouse
│   └── capture.py           # Captura da região selecionada
├── ocr/
│   └── reader.py            # OCRReader (base) e TesseractReader
├── translation/
│   └── translator.py        # Translator (base), Google e MyMemory
└── ui/
    └── overlay.py           # Janela que exibe a tradução
```

OCR e tradução usam uma **classe base** (`OCRReader`, `Translator`) com implementações concretas. Para trocar o motor (por exemplo, EasyOCR no lugar do Tesseract, ou DeepL no lugar do MyMemory), basta criar uma nova classe; o resto do código não muda.

## Limitações conhecidas

- **MyMemory** tem limite gratuito de cerca de 5 mil caracteres por dia e não detecta o idioma de origem sozinho.
- **Google Tradutor** (via `deep-translator`) pode responder `TooManyRequests` em algumas redes (VPN, redes corporativas), mesmo na primeira requisição.
- **Texto animado ou fundo que muda** pode fazer o OCR ler variações do mesmo texto e gerar traduções repetidas.
- **Área colada no topo da tela**: a janela de tradução não tem espaço para subir e pode cobrir a área capturada.
- **Wayland (Linux)**: a captura de tela pode retornar imagem preta; use uma sessão X11.

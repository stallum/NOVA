# N.O.V.A. — Project README

This README documents the N.O.V.A. project (Núcleo Organizador de Verbetes e Anotações). The file contains two language sections: English and Portuguese. It describes the technologies, architecture, programming logic, how to run and extend the project, environment variables, and suggested next steps.

## English

### Overview

N.O.V.A. is a small command-line oriented assistant designed to triage user requests and create concise notes from different input types such as YouTube videos and PDF documents. The application orchestrates several utilities to download and process media, transcribe audio, summarize content and create notes.

The codebase present in the `app/` folder contains a simple agent-driven workflow: a triage step that classifies incoming user prompts into one of: VIDEO_YT, PDF, or INFO, then runs the appropriate processing steps and finally generates a note or summary.

### Technologies & Libraries

- Python (tested with modern 3.x — e.g. 3.11+ recommended)
- langchain-google-genai (ChatGoogleGenerativeAI) — used for LLM-driven triage and structured outputs
- langchain-core, langgraph — for message types and constructing a StateGraph workflow
- pydantic — typed model for structured LLM output
- python-dotenv — load environment variables from a .env file
- standard Python libraries: `re`, `json`, `typing`

Note: Some third-party modules referenced (for example, `langchain_google_genai`, `langgraph`) may require provider-specific credentials and setup (Google Cloud / Vertex AI or similar). Check package docs for installation and authentication steps.

### Project Structure

- `app/main.py` — (entry point) currently the project's executable script that can launch the agent/workflow.
- `app/utils/agente.py` — defines the agent workflow, nodes, triage prompt, and the compiled StateGraph. This file wires together the LLM triager and modules that perform specific jobs (YouTube summarization, PDF reading, and note generation).
- `app/utils/video_summarize.py` — helper for downloading/transcribing YouTube videos and extracting audio (implementation in repository).
- `app/utils/pdf_reader.py` — helper for loading and extracting text from PDFs.
- `app/utils/notas.py` — helper for creating notes (summaries, formatting or storing results).
- `app/utils/styling.py` — utility for terminal or output styling (if present).

### Core Logic and Flow

1. The user provides a prompt (for example: "summarize this video for me").
2. `agente.py` uses `ChatGoogleGenerativeAI` to run a triage prompt (`PROMPT_MENU`) which returns structured JSON indicating one of three decisions: `VIDEO_YT`, `PDF`, or `INFO` and any missing fields.
3. Based on the decision, the StateGraph routes the execution to a node:
   - `youtube` node: prompts user for a YouTube link, downloads the video, extracts audio, and transcribes it.
   - `pdf` node: prompts user for a PDF path and extracts text.
   - `resumo` node: creates a note/summary using the text produced by previous nodes.
4. Final output is a summarized note or an informational message depending on the triage result.

### Inputs, Outputs and Data Shapes

- Triage Output: JSON with shape { "decisao": "VIDEO_YT" | "PDF" | "INFO", "campos_faltantes": [string] }
- Agent State: a small dict/TypedDict with optional keys: `pergunta`, `triagem`, `texto`, `result`.

### Environment & Credentials

Create a `.env` file in the project root or set environment variables in your system. Common variables you will likely need (examples):

- GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS — for Google/Vertex AI authentication (if using that backend)
- Any other provider-specific keys required by the libraries you use (check each library's docs)

Load env variables using python-dotenv (already present in `agente.py`).

### How to Run (basic)

1. Create a virtual environment and install dependencies. Since this repository does not include a `requirements.txt`, create one or install manually. Example (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install python-dotenv pydantic
# Install the rest according to your chosen LLM and media-processing libraries
```

2. Set required environment variables (or create `.env`).

3. Run the agent from the `app/` folder: `python app/utils/agente.py` or run `app/main.py` if it exists as the intended entrypoint.

Note: The agent uses `input()` to ask for links or file paths during the workflow.

### Edge Cases & Considerations

- Missing inputs: The triage step can return `campos_faltantes` — ensure the application requests missing fields from the user before proceeding.
- Long media: Downloading and transcribing long videos may take significant time and memory. Consider streaming or chunked transcription.
- Error handling: Several operations (network, file I/O, LLM calls) need robust try/except blocks with retry/backoff.
- Authentication: Ensure API keys and credentials are set and that quota limits are considered.

### Suggested Improvements

- Add a `requirements.txt` or `pyproject.toml` to lock dependencies.
- Replace blocking `input()` calls with a small CLI (argparse / Typer) or web UI for better UX and automation.
- Add logging and configurable verbosity levels instead of prints.
- Add unit tests for each util in `app/utils/` (use pytest).
- Add a simple caching layer for transcriptions to avoid repeating work.

### Development Checklist / Contract

- Inputs: user text prompt (string), YouTube link (string) or PDF path (string).
- Outputs: structured note (string) and possibly a saved file.
- Error modes: missing credentials, invalid link/path, network failure, LLM errors.

### Quick Troubleshooting

- If the LLM fails with authentication errors, verify `GOOGLE_APPLICATION_CREDENTIALS` or other provider variables.
- If YouTube download fails, ensure youtube-dl/yt-dlp or equivalent tools are installed and available to `video_summarize.py` implementation.

## Português (Portuguese)

### Visão geral

N.O.V.A. é um assistente orientado a linha de comando que triageia pedidos de usuários e cria notas a partir de entradas como vídeos do YouTube e arquivos PDF. O projeto orquestra utilitários para baixar e processar mídia, transcrever áudio, resumir conteúdo e gerar notas.

O código dentro da pasta `app/` define um fluxo simples orientado por um agente: primeiro uma triagem que classifica a mensagem do usuário em `VIDEO_YT`, `PDF` ou `INFO`, depois executa os passos de processamento apropriados e, por fim, gera uma nota ou resumo.

### Tecnologias e bibliotecas

- Python (recomendado 3.x moderno, ex.: 3.11+)
- langchain-google-genai (ChatGoogleGenerativeAI) — usado para triagem por LLM e saída estruturada
- langchain-core, langgraph — tipos de mensagem e construção do StateGraph
- pydantic — modelos tipados para saída estruturada do LLM
- python-dotenv — carregar variáveis de ambiente a partir de um arquivo .env
- bibliotecas padrão do Python: `re`, `json`, `typing`

Observação: Alguns pacotes de terceiros (por exemplo, `langchain_google_genai`, `langgraph`) podem requerer credenciais de provedores (Google Cloud / Vertex AI). Consulte a documentação dos pacotes para instalar e autenticar.

### Estrutura do projeto

- `app/main.py` — ponto de entrada (script) que executa o agente/fluxo.
- `app/utils/agente.py` — define o fluxo do agente, nós, prompt de triagem e o StateGraph compilado; conecta o triador LLM com utilitários de processamento (vídeo, PDF, notas).
- `app/utils/video_summarize.py` — utilitário para baixar/transcrever vídeos do YouTube e extrair áudio.
- `app/utils/pdf_reader.py` — utilitário para carregar e extrair texto de PDFs.
- `app/utils/notas.py` — utilitário para criar notas (formatar, resumir ou salvar resultados).
- `app/utils/styling.py` — utilitário para estilização de saída/terminal (se presente).

### Lógica principal e fluxo

1. O usuário fornece uma pergunta ou pedido (ex.: "resume esse video para mim").
2. `agente.py` usa `ChatGoogleGenerativeAI` com o `PROMPT_MENU` para retornar JSON estruturado indicando a decisão: `VIDEO_YT`, `PDF` ou `INFO` e os campos faltantes.
3. O StateGraph direciona a execução a um nó:
   - nó `youtube`: solicita link do YouTube, baixa o vídeo, extrai áudio e transcreve.
   - nó `pdf`: solicita caminho do arquivo PDF e extrai o texto.
   - nó `resumo`: cria a nota/resumo com o texto obtido.
4. A saída final é uma nota resumida ou uma mensagem informativa, dependendo da triagem.

### Entradas, saídas e formatos de dados

- Saída da triagem: JSON com formato { "decisao": "VIDEO_YT" | "PDF" | "INFO", "campos_faltantes": [string] }
- Estado do agente: dict/TypedDict com chaves opcionais: `pergunta`, `triagem`, `texto`, `result`.

### Ambiente e credenciais

Crie um arquivo `.env` na raiz do projeto ou configure variáveis de ambiente no sistema. Variáveis comuns necessárias:

- GOOGLE_API_KEY ou GOOGLE_APPLICATION_CREDENTIALS — para autenticação com Google/Vertex AI (se aplicável)
- Outras chaves de provedores conforme exigido pelas bibliotecas utilizadas

As variáveis são carregadas via python-dotenv (veja `agente.py`).

### Como executar (essencial)

1. Crie um ambiente virtual e instale dependências. Não existe um `requirements.txt` no repositório, portanto crie um ou instale manualmente. Exemplo (PowerShell Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install python-dotenv pydantic
# Instale o restante conforme bibliotecas de LLM e processamento de mídia
```

2. Configure as variáveis de ambiente ou um arquivo `.env`.

3. Execute o agente: `python app/utils/agente.py` ou `python app/main.py` dependendo do ponto de entrada desejado.

# obs: readme temporário feito por IA
# temporary readme made by AI

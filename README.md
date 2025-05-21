# 🗣️ Transcrição e Tradução de Áudio com IA

Este projeto utiliza **inteligência artificial** para **transcrever áudios em português** e **traduzir o texto** para diversos idiomas com alta precisão. Ele combina o poder da **transcrição offline com Vosk** e **tradução via Gemini 1.5 (Google)**, tudo isso em uma interface web simples usando **Streamlit**.

---

## 🚀 Funcionalidades

- 🎧 **Upload de arquivos MP3**
- 📝 **Transcrição offline** com [Vosk](https://alphacephei.com/vosk/)
- 🌐 **Tradução inteligente** com o modelo **Gemini 1.5 Flash**
- 🖥️ **Interface web responsiva** com Streamlit
- ✅ **Funciona offline para transcrição** (não precisa de conexão com a internet)

---

## 🧠 Tecnologias e Bibliotecas

| Biblioteca | Função |
|-----------|--------|
| `streamlit` | Criação da interface web interativa |
| `pydub` | Conversão e processamento de arquivos de áudio |
| `vosk` | Transcrição de áudio offline com reconhecimento de fala |
| `google.generativeai` | Acesso à API Gemini para tradução |
| `dotenv` | Gerenciamento de variáveis de ambiente (API key) |
| `wave`, `json`, `re`, `os` | Utilitários padrão do Python |

---

## 🧩 Instalação

1. Clone o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

2. Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instale as dependências:
pip install -r requirements.txt

Baixe o modelo Vosk de reconhecimento de fala (Português):

4. Acesse: https://alphacephei.com/vosk/models

Recomendo o modelo: vosk-model-small-pt-0.3
Descompacte a pasta e renomeie para model, colocando-a na raiz do projeto.

5. Crie um arquivo .env na raiz com sua chave da API Gemini:

GEMINI_API_KEY=sua_chave_aqui

# Execute com:

streamlit run app.py


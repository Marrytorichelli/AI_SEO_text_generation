## SEO Text Generation RAG System

### Overview
RAG-система для генерации SEO-статей (~6000 слов) на английском языке на основе технических заданий на русском. Используется векторный поиск по эталонным текстам (ChromaDB + OpenAI embeddings) и генерация через Claude Sonnet 4.

### Features
- Векторная БД на ChromaDB c OpenAI embeddings (text-embedding-3-small)
- Генерация через Claude Sonnet 4 (Anthropic)
- Поддержка .txt и .docx (для эталонов и ТЗ)
- Автоматическое связывание ТЗ и эталонных текстов по имени файла
- Batch-генерация множества статей и сохранение результатов в output/

### Project Structure
- `src/embeddings.py` — управление эмбеддингами и ChromaDB (OpenAIEmbeddings)
- `src/setup_vectorstore.py` — первичная загрузка данных и построение ChromaDB
- `src/generator.py` — RAG-генерация SEO-текстов (Claude Sonnet 4)
- `src/data_loader.py` — вспомогательная загрузка текстов (если требуется)
- `main.py` — CLI (ингест/генерация) при необходимости
- `data/texts/` — эталонные тексты (EN)
- `data/tz/` — технические задания (RU)
- `chroma_db/` — директория ChromaDB
- `output/` — результаты генерации

### Prerequisites
- Python 3.11 (рекомендуется; 3.13 может вызывать несовместимости)
- OpenAI API key (для embeddings)
- Anthropic API key (для Claude Sonnet 4)

### Installation

#### 1. Clone and setup environment
```bash
git clone <repo-url>
cd ANB-5577
python -m venv venv
# Windows PowerShell
./venv/Scripts/Activate.ps1
# Linux/Mac
source venv/bin/activate
```

#### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure environment
Создайте файл `.env` в корне проекта, если файл создан, добавьте ваши API ключи:
```bash
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### 4. Prepare data (для обучения)
Поместите файлы:
- Эталонные тексты (English) → `data/texts/`
- Технические задания (Russian) → `data/tz/`

Важно: имена файлов ТЗ и текстов должны совпадать (без расширения).
Пример:
```text
data/texts/article-name.docx
data/tz/article-name.txt
```

### Usage

#### 1. Create vector database (one-time setup)
```bash
python src/setup_vectorstore.py
```

#### 2. Generate single article
Простейший тест (пример):
```bash
python test_generation.py
```
или непосредственно из своего скрипта:
```bash
python generate_article.py "data/tz/your-tz-file.txt"
```

#### 3. Batch generation (запускается для генерации статей, ТЗ должно быть в папке ./data/tz/)
```bash
python batch_generate.py
```
Результаты сохраняются в папку `output/`.

### Configuration

#### Embedding settings (`src/embeddings.py`)
- Model: `text-embedding-3-small` (OpenAI)
- Chunk size: 2000 characters
- Chunk overlap: 400 characters

#### Generation settings (`src/generator.py`)
- Model: `claude-sonnet-4-20250514`
- Temperature: 0.7
- Max tokens: 8000
- Target: ~6000 words per article

### Key Components
- `embeddings.py` — управление векторными представлениями и ChromaDB
- `setup_vectorstore.py` — создание векторной БД из эталонных текстов и ТЗ, логирование и статистика
- `generator.py` — основная логика RAG и вызов Claude, промпт с жестким требованием писать на EN

### Troubleshooting
- ModuleNotFoundError при запуске
  ```bash
  pip install --no-cache-dir -r requirements.txt
  ```
- Python 3.13 compatibility issues
  Используйте Python 3.11:
  ```bash
  py -3.11 -m venv venv
  ```
- ChromaDB errors / некорректный индекс
  Удалите существующую БД и пересоздайте:
  ```bash
  rm -rf chroma_db/
  python src/setup_vectorstore.py
  ```
- Missing OPENAI_API_KEY / ANTHROPIC_API_KEY
  Убедитесь, что ключи прописаны в `.env` и загружаются через `load_dotenv()`.
- tqdm отсутствует
  Скрипты либо гибко обходят отсутствие tqdm, либо установите:
  ```bash
  pip install tqdm
  ```
- Импорт langchain/совместимость пакетов
  Устанавливайте по одному или используйте версии из `requirements.txt`. На Windows иногда помогает флаг `--user`:
  ```bash
  python -m pip install --user -r requirements.txt
  ```

### Cost Estimation (rough)
- Vector DB creation (one-time): ~$0.10 (зависит от объема)
- Generation (per ~6000-word article): ~$0.05–0.08
- Batch of 100 articles: ~$8–10

### Dependencies
Основные библиотеки:
- langchain (см. `requirements.txt`)
- langchain-openai (OpenAI embeddings)
- langchain-anthropic (Claude)
- chromadb
- openai / anthropic SDKs

Полный список — в `requirements.txt`.

### Notes
- ТЗ на русском, генерация строго на английском (US English)
- Система автоматически подмешивает похожие эталонные тексты
- Результаты соответствуют структуре и стилю примеров
- Рекомендуется Python 3.11 для стабильности окружения




from src.embeddings import EmbeddingManager

# Загрузка векторной БД
manager = EmbeddingManager()
vectorstore = manager.load_vectorstore()

# Тестовый запрос (на русском - как ваши ТЗ)
query = "как конвертировать видео в MP4"

# Поиск похожих текстов
results = vectorstore.similarity_search(
    query, 
    k=3,
    filter={"type": "reference_text"}  # Ищем только готовые тексты
)

print(f"Найдено {len(results)} похожих текстов:\n")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.metadata.get('filename')}")
    print(f"   Язык: {doc.metadata.get('language')}")
    print(f"   Слов: {doc.metadata.get('word_count')}")
    print(f"   Превью: {doc.page_content[:200]}...\n")
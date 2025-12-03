from src.embeddings import EmbeddingManager

# Загрузка БД
manager = EmbeddingManager()
vectorstore = manager.load_vectorstore()

# Проверка количества документов
collection = vectorstore._collection
print(f"📊 Всего эмбеддингов в БД: {collection.count()}")

# Тестовый поиск
query = "как выбрать продукт"  # пример на русском
results = vectorstore.similarity_search(query, k=3)

print(f"\n🔍 Результаты поиска для '{query}':")
for i, doc in enumerate(results, 1):
    print(f"\n{i}. {doc.metadata.get('filename', 'unknown')}")
    print(f"   Type: {doc.metadata.get('type')}")
    print(f"   Language: {doc.metadata.get('language')}")
    print(f"   Preview: {doc.page_content[:100]}...")
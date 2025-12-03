from src.generator import create_generator

# Тестовое ТЗ
# test_tz = """
# Тема: Как конвертировать DVD в MP4
# Ключевые слова: конвертировать dvd в mp4, dvd to mp4, преобразовать dvd
# Объем: 6000 слов
# Структура: введение, способы конвертации, пошаговые инструкции, FAQ
# """
test_tz = """
LANGUAGE: Write the article in ENGLISH (US English)

Тема: Как конвертировать DVD в MP4
Ключевые слова: convert dvd to mp4, dvd converter, dvd to mp4 converter
Объем: 1000 слов
Структура: introduction, conversion methods, step-by-step guide, conclusion

IMPORTANT: The article must be written in English, even though this brief is in Russian.
"""
# Создание генератора
generator = create_generator()

# Генерация текста
print("Генерация началась...")
result = generator.generate(test_tz)

print(f"\nГотово!")
print(f"Слов: {result['word_count']}")
print(f"Использовано примеров: {result['examples_used']}")
print(f"\nПервые 500 символов:\n{result['text'][:500]}...")

# Сохранение
generator.save_result(result, "output/test_article.txt")
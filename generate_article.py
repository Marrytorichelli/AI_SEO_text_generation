import sys
from pathlib import Path
from src.generator import create_generator

if len(sys.argv) < 2:
    print("Использование: python generate_article.py путь/к/тз.txt")
    sys.exit(1)

tz_path = Path(sys.argv[1])
if not tz_path.exists():
    print(f"Файл не найден: {tz_path}")
    sys.exit(1)

# Читаем ТЗ
tz_text = tz_path.read_text(encoding='utf-8')

print(f"Генерация по ТЗ: {tz_path.name}")
print("=" * 50)

generator = create_generator()
result = generator.generate(tz_text)

# Сохраняем результат
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

output_path = output_dir / f"{tz_path.stem}_generated.txt"
generator.save_result(result, str(output_path))

print(f"\n✅ Статья сохранена: {output_path}")
print(f"Слов: {result['word_count']}")
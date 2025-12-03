# from pathlib import Path
# from src.generator import create_generator
# from tqdm import tqdm

# tz_dir = Path("data/tz")
# output_dir = Path("output")
# output_dir.mkdir(exist_ok=True)

# tz_files = list(tz_dir.glob("*.txt"))
# print(f"Найдено {len(tz_files)} файлов ТЗ")

# generator = create_generator()

# for tz_file in tqdm(tz_files, desc="Генерация"):
#     tz_text = tz_file.read_text(encoding='utf-8')
    
#     try:
#         result = generator.generate(tz_text)
        
#         output_path = output_dir / f"{tz_file.stem}_generated.txt"
#         generator.save_result(result, str(output_path))
        
#         print(f"✅ {tz_file.name}: {result['word_count']} слов")
        
#     except Exception as e:
#         print(f"❌ Ошибка в {tz_file.name}: {e}")

# print("\n✅ Batch генерация завершена!")
from pathlib import Path
from src.generator import create_generator
from tqdm import tqdm
import time

tz_dir = Path("data/tz")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Ищем только .txt файлы с ТЗ (пропускаем example файлы)
tz_files = [f for f in tz_dir.glob("*.txt") if "example" not in f.stem.lower()]
print(f"Найдено {len(tz_files)} файлов ТЗ для обработки\n")

generator = create_generator()

results = []
total_words = 0
total_time = 0

for tz_file in tqdm(tz_files, desc="Генерация статей"):
    tz_text = tz_file.read_text(encoding='utf-8')
    
    try:
        start = time.time()
        result = generator.generate(tz_text)
        gen_time = time.time() - start
        
        output_path = output_dir / f"{tz_file.stem}_generated.txt"
        generator.save_result(result, str(output_path))
        
        total_words += result['word_count']
        total_time += gen_time
        
        results.append({
            'file': tz_file.name,
            'words': result['word_count'],
            'time': gen_time,
            'status': 'success'
        })
        
        tqdm.write(f"✅ {tz_file.name}: {result['word_count']} words in {gen_time:.1f}s")
        
    except Exception as e:
        results.append({
            'file': tz_file.name,
            'error': str(e),
            'status': 'failed'
        })
        tqdm.write(f"❌ {tz_file.name}: {e}")

# Итоги
print("\n" + "="*60)
print("ИТОГИ ГЕНЕРАЦИИ:")
print("="*60)
success = sum(1 for r in results if r['status'] == 'success')
failed = sum(1 for r in results if r['status'] == 'failed')
print(f"Успешно: {success}/{len(tz_files)}")
print(f"Ошибки: {failed}")
print(f"Всего слов: {total_words:,}")
print(f"Общее время: {total_time/60:.1f} минут")
if success > 0:
    print(f"Среднее время на статью: {total_time/success:.1f} секунд")
    print(f"Средняя длина: {total_words/success:.0f} слов")
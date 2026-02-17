# -*- coding: utf-8 -*-
"""
Скрипт для массового исправления путей во всех статьях Акта 2019-12
Исправляет:
1. Пути к CSS (из-за изменения структуры папок)
2. Ссылки на оглавление (act-2019.html → act-2019-12.html)
"""

import os
import re
from pathlib import Path

def fix_paths_in_file(file_path):
    """Исправляет пути в одном HTML-файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = []

        # 1. Исправляем пути к CSS
        # Было: ../../../css/
        # Должно быть: ../../../../css/ (добавляем ещё один уровень вверх)
        if '../../../css/' in content:
            content = content.replace('../../../css/', '../../../../css/')
            changes_made.append('Исправлены пути к CSS')

        # 2. Исправляем ссылки на оглавление
        # Было: ../act-2019.html
        # Должно быть: ../act-2019-12.html
        content = re.sub(
            r'href="(\.\./)?act-2019\.html"',
            r'href="\1act-2019-12.html"',
            content
        )
        if 'act-2019.html' not in content and 'act-2019-12.html' in original_content:
            changes_made.append('Исправлены ссылки на оглавление')
        elif 'act-2019.html' not in content:
            changes_made.append('Исправлены ссылки на оглавление')

        # 3. Исправляем breadcrumb
        # Было: <a href="../act-2019.html">Госакт 2019</a>
        # Должно быть: <a href="../act-2019-12.html">Госакт 2019-12</a>
        content = re.sub(
            r'<a href="(\.\./)?act-2019\.html">Госакт 2019</a>',
            r'<a href="\1act-2019-12.html">Госакт 2019-12</a>',
            content
        )

        # 4. Исправляем текст "Оглавление Акта 2019"
        content = content.replace('Оглавление Акта 2019', 'Оглавление Акта 2019-12')
        content = content.replace('Госакт 2019', 'Госакт 2019-12')

        # 5. Исправляем пути к index.html (если нужно)
        # Было: ../../../index.html
        # Должно быть: ../../../../index.html
        if '../../../index.html' in content:
            content = content.replace('../../../index.html', '../../../../index.html')
            changes_made.append('Исправлены пути к index.html')

        # 6. Исправляем пути к glossary.html и references.html
        if '../../../glossary.html' in content:
            content = content.replace('../../../glossary.html', '../../../../glossary.html')
            changes_made.append('Исправлены пути к glossary.html')

        if '../../../references.html' in content:
            content = content.replace('../../../references.html', '../../../../references.html')
            changes_made.append('Исправлены пути к references.html')

        # Сохраняем изменения, если были
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        else:
            return False, []

    except Exception as e:
        print(f"❌ Ошибка при обработке {file_path}: {str(e)}")
        return False, []

def main():
    """Основная функция"""
    print("🔧 Начинаю исправление путей во всех статьях...\n")
    print("=" * 80)

    # Пути к папке со статьями
    possible_paths = [
        Path("documents/2019/act-2019-12/articles"),
        Path("documents/act-2019/articles"),
        Path("articles")
    ]

    articles_dir = None
    for path in possible_paths:
        if path.exists():
            articles_dir = path
            break

    if not articles_dir:
        print("❌ Ошибка: Папка со статьями не найдена!")
        print("\nПопробуйте запустить скрипт из корня репозитория")
        return

    print(f"📁 Папка найдена: {articles_dir}\n")
    print("=" * 80 + "\n")

    # Счётчики
    total_files = 0
    fixed_files = 0
    skipped_files = 0

    # Обрабатываем Преамбулу
    preamble_file = articles_dir / "preamble.html"
    if preamble_file.exists():
        total_files += 1
        fixed, changes = fix_paths_in_file(preamble_file)
        if fixed:
            print(f"✅ preamble.html — исправлено")
            for change in changes:
                print(f"   • {change}")
            fixed_files += 1
        else:
            print(f"⚪ preamble.html — изменений не требуется")
            skipped_files += 1

    # Обрабатываем Введение
    intro_file = articles_dir / "intro.html"
    if intro_file.exists():
        total_files += 1
        fixed, changes = fix_paths_in_file(intro_file)
        if fixed:
            print(f"✅ intro.html — исправлено")
            for change in changes:
                print(f"   • {change}")
            fixed_files += 1
        else:
            print(f"⚪ intro.html — изменений не требуется")
            skipped_files += 1

    print("\n" + "=" * 80 + "\n")

    # Обрабатываем статьи 1-60
    for i in range(1, 61):
        article_num = str(i).zfill(2)
        article_file = articles_dir / f"article-{article_num}.html"

        if article_file.exists():
            total_files += 1
            fixed, changes = fix_paths_in_file(article_file)
            if fixed:
                print(f"✅ article-{article_num}.html — исправлено")
                if i <= 5:  # Показываем детали только для первых 5 статей
                    for change in changes:
                        print(f"   • {change}")
                fixed_files += 1
            else:
                if i <= 5:
                    print(f"⚪ article-{article_num}.html — изменений не требуется")
                skipped_files += 1
        else:
            print(f"⚠️  article-{article_num}.html — файл не найден")

    print("\n" + "=" * 80)
    print(f"\n📊 ИТОГИ:\n")
    print(f"   Обработано файлов: {total_files}")
    print(f"   ✅ Исправлено: {fixed_files}")
    print(f"   ⚪ Без изменений: {skipped_files}")
    print("\n" + "=" * 80)
    print("\n🎉 Готово! Все пути исправлены!")
    print("\nТеперь можно:")
    print("  1. Проверить несколько статей в браузере")
    print("  2. Закоммитить и запушить изменения на GitHub")
    print("  3. Проверить сайт: https://pesh1111111-cmyk.github.io/encyclopedia-Gosact/")

if __name__ == "__main__":
    main()
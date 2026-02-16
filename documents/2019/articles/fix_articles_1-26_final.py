#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ФИНАЛЬНЫЙ ФИКСЕР для статей 1-26:
1. Убирает style="display: none;" из оригинального текста
2. Перемещает блок оригинального текста ПОСЛЕ summary-box
3. Удаляет кнопку view-toggle
4. Удаляет ссылку на article-viewer.js
"""

import os
import re

# Список файлов
files_to_fix = [
    "preamble.html",
    "intro.html",
] + [f"article-{i:02d}.html" for i in range(1, 27)]


def fix_article(filename):
    if not os.path.exists(filename):
        print(f"⚠️  Файл не найден: {filename}")
        return False

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # ШАГ 1: Находим блок оригинального текста (весь блок)
        original_pattern = r'(\s*)<div class="original-text-block"[^>]*>.*?</div>(\s*)'
        original_match = re.search(original_pattern, content, re.DOTALL)

        if not original_match:
            print(f"⚠️  Блок оригинального текста не найден: {filename}")
            return False

        original_block = original_match.group(0)

        # Убираем style="display: none;" если есть
        original_block_fixed = re.sub(
            r'<div class="original-text-block" id="originalText" style="display: none;">',
            r'<div class="original-text-block">',
            original_block
        )

        # ШАГ 2: Удаляем оригинальный блок из старого места
        content = re.sub(original_pattern, '', content, count=1, flags=re.DOTALL)

        # ШАГ 3: Находим конец summary-box и вставляем туда оригинальный текст
        # Ищем закрывающий </div> блока summary-box
        summary_pattern = r'(</div>\s*</div>\s*)(<div class="article-text">)'

        if re.search(summary_pattern, content):
            content = re.sub(
                summary_pattern,
                rf'\1\n{original_block_fixed}\n\2',
                content,
                count=1
            )
        else:
            print(f"⚠️  Не найден паттерн для вставки: {filename}")
            return False

        # ШАГ 4: Удаляем блок с кнопкой view-toggle
        content = re.sub(
            r'\s*<div class="view-toggle">.*?</div>\s*',
            '\n',
            content,
            flags=re.DOTALL
        )

        # ШАГ 5: Удаляем ссылку на article-viewer.js
        content = re.sub(
            r'\s*<script src="../../../js/article-viewer.js"></script>\s*',
            '\n',
            content
        )

        # Проверка изменений
        if content == original_content:
            print(f"ℹ️  Файл не изменён: {filename}")
            return True

        # Сохраняем
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Исправлен: {filename}")
        return True

    except Exception as e:
        print(f"❌ Ошибка {filename}: {e}")
        return False


def main():
    print("=" * 70)
    print("🔧 ФИНАЛЬНЫЙ ФИКСЕР ДЛЯ СТАТЕЙ 1-26")
    print("=" * 70)
    print("Что делает:")
    print("  1. ✅ Убирает style='display: none;' из оригинального текста")
    print("  2. ✅ Перемещает оригинал ПОСЛЕ 'Краткое содержание'")
    print("  3. ✅ Перемещает оригинал ПЕРЕД 'Структурированный разбор'")
    print("  4. ✅ Удаляет кнопку 'Показать оригинальный текст'")
    print("  5. ✅ Удаляет ссылку на article-viewer.js")
    print("=" * 70)
    print()

    fixed = 0
    errors = 0
    not_found = 0

    for filename in files_to_fix:
        if not os.path.exists(filename):
            not_found += 1
            continue

        if fix_article(filename):
            fixed += 1
        else:
            errors += 1

    print()
    print("=" * 70)
    print(f"🎉 ГОТОВО!")
    print(f"✅ Исправлено: {fixed}")
    print(f"⚠️  Не найдено: {not_found}")
    print(f"❌ Ошибок: {errors}")
    print("=" * 70)


if __name__ == "__main__":
    main()
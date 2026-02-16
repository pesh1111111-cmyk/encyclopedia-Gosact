#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматическое исправление статей 1-26:
Убирает кнопку переключения и делает оригинальный текст видимым сразу
"""

import os
import re

# Список файлов для исправления
files_to_fix = [
    "preamble.html",
    "intro.html",
] + [f"article-{i:02d}.html" for i in range(1, 27)]


def fix_article(filename):
    """
    Исправляет один HTML-файл:
    1. Убирает style="display: none;" из блока оригинального текста
    2. Удаляет блок с кнопкой переключения
    3. Удаляет ссылку на article-viewer.js
    """

    if not os.path.exists(filename):
        print(f"⚠️  Файл не найден: {filename}")
        return False

    try:
        # Читаем файл
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # ИСПРАВЛЕНИЕ 1: Убираем style="display: none;" из блока оригинального текста
        content = re.sub(
            r'<div class="original-text-block" id="originalText" style="display: none;">',
            r'<div class="original-text-block">',
            content
        )

        # ИСПРАВЛЕНИЕ 2: Убираем весь блок с кнопкой переключения
        # Ищем блок от <div class="view-toggle"> до </div>
        content = re.sub(
            r'<div class="view-toggle">.*?</div>\s*',
            '',
            content,
            flags=re.DOTALL
        )

        # ИСПРАВЛЕНИЕ 3: Убираем ссылку на article-viewer.js
        content = re.sub(
            r'<script src="../../../js/article-viewer.js"></script>\s*',
            '',
            content
        )

        # Проверяем, изменился ли контент
        if content == original_content:
            print(f"ℹ️  Файл уже исправлен: {filename}")
            return True

        # Сохраняем исправленный файл
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Исправлен: {filename}")
        return True

    except Exception as e:
        print(f"❌ Ошибка при исправлении {filename}: {e}")
        return False


def main():
    print("🔧 СКРИПТ-ФИКСЕР ДЛЯ СТАТЕЙ 1-26")
    print("=" * 50)
    print("Что делает скрипт:")
    print("  1. Убирает style='display: none;' из оригинального текста")
    print("  2. Удаляет кнопку 'Показать оригинальный текст'")
    print("  3. Удаляет ссылку на article-viewer.js")
    print("=" * 50)
    print()

    fixed_count = 0
    not_found_count = 0
    error_count = 0

    for filename in files_to_fix:
        if not os.path.exists(filename):
            not_found_count += 1
            continue

        if fix_article(filename):
            fixed_count += 1
        else:
            error_count += 1

    print()
    print("=" * 50)
    print(f"🎉 ГОТОВО!")
    print(f"✅ Исправлено файлов: {fixed_count}")
    print(f"⚠️  Не найдено файлов: {not_found_count}")
    print(f"❌ Ошибок: {error_count}")
    print("=" * 50)

    if not_found_count > 0:
        print()
        print("💡 СОВЕТ: Убедитесь, что вы запускаете скрипт")
        print("   в папке documents/2019/articles/")


if __name__ == "__main__":
    main()
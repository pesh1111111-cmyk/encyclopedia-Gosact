#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
УЛУЧШЕННЫЙ ФИКСЕР v2 для статей 1-26
Использует более простой и надёжный подход
"""

import os
import re

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
            lines = f.readlines()

        # Ищем ключевые строки
        summary_end_idx = None
        article_text_start_idx = None
        original_start_idx = None
        original_end_idx = None
        view_toggle_start_idx = None
        view_toggle_end_idx = None
        script_idx = None

        for i, line in enumerate(lines):
            # Конец summary-box
            if '</div>' in line and summary_end_idx is None:
                # Проверяем, что это действительно конец summary-box
                # Ищем в предыдущих 20 строках 'summary-box'
                context = ''.join(lines[max(0, i-20):i+1])
                if 'summary-box' in context and 'article-text' not in context:
                    summary_end_idx = i

            # Начало article-text
            if '<div class="article-text">' in line:
                article_text_start_idx = i

            # Начало original-text-block
            if '<div class="original-text-block"' in line:
                original_start_idx = i

            # Конец original-text-block (первый </div> после начала)
            if original_start_idx is not None and original_end_idx is None:
                if '</div>' in line and i > original_start_idx:
                    # Проверяем, сколько <div> и </div> между началом и текущей позицией
                    block = ''.join(lines[original_start_idx:i+1])
                    open_count = block.count('<div')
                    close_count = block.count('</div>')
                    if open_count == close_count:
                        original_end_idx = i

            # Блок view-toggle
            if '<div class="view-toggle">' in line:
                view_toggle_start_idx = i

            if view_toggle_start_idx is not None and view_toggle_end_idx is None:
                if '</div>' in line and i > view_toggle_start_idx:
                    view_toggle_end_idx = i

            # Скрипт article-viewer.js
            if 'article-viewer.js' in line:
                script_idx = i

        print(f"\n🔍 Анализ {filename}:")
        print(f"   summary_end: {summary_end_idx}")
        print(f"   article_text_start: {article_text_start_idx}")
        print(f"   original: {original_start_idx} - {original_end_idx}")
        print(f"   view_toggle: {view_toggle_start_idx} - {view_toggle_end_idx}")
        print(f"   script: {script_idx}")

        if original_start_idx is None or original_end_idx is None:
            print(f"⚠️  Не найден блок оригинального текста: {filename}")
            return False

        if article_text_start_idx is None:
            print(f"⚠️  Не найден блок article-text: {filename}")
            return False

        # ПЛАН ДЕЙСТВИЙ:
        # 1. Извлекаем блок оригинального текста
        # 2. Удаляем style="display: none;" если есть
        # 3. Удаляем блок оригинала из старого места
        # 4. Вставляем его ПЕРЕД article-text
        # 5. Удаляем view-toggle
        # 6. Удаляем script

        # Извлекаем оригинальный блок
        original_block = lines[original_start_idx:original_end_idx+1]

        # Убираем style="display: none;"
        original_block_fixed = []
        for line in original_block:
            line_fixed = line.replace('style="display: none;"', '')
            line_fixed = line_fixed.replace('id="originalText" ', '')
            original_block_fixed.append(line_fixed)

        # Создаём новый список строк
        new_lines = []

        i = 0
        while i < len(lines):
            # Пропускаем оригинальный блок в старом месте
            if i == original_start_idx:
                i = original_end_idx + 1
                continue

            # Пропускаем view-toggle
            if view_toggle_start_idx is not None and i == view_toggle_start_idx:
                i = view_toggle_end_idx + 1
                continue

            # Пропускаем script
            if script_idx is not None and i == script_idx:
                i += 1
                continue

            # Вставляем оригинальный блок ПЕРЕД article-text
            if i == article_text_start_idx:
                new_lines.append('\n')
                new_lines.extend(original_block_fixed)
                new_lines.append('\n')

            new_lines.append(lines[i])
            i += 1

        # Сохраняем
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"✅ Исправлен: {filename}")
        return True

    except Exception as e:
        print(f"❌ Ошибка {filename}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 70)
    print("🔧 УЛУЧШЕННЫЙ ФИКСЕР v2 ДЛЯ СТАТЕЙ 1-26")
    print("=" * 70)
    print()

    fixed = 0
    errors = 0
    not_found = 0

    for filename in files_to_fix:
        if not os.path.exists(filename):
            not_found += 1
            print(f"⚠️  Не найден: {filename}")
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
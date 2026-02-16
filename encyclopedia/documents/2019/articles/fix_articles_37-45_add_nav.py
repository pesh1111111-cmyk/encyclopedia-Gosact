#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавление ссылок на глоссарий и справки в шапку статей 37-45
"""

import os
import re

files_to_fix = [f"article-{i:02d}.html" for i in range(37, 46)]

def fix_nav(filename):
    if not os.path.exists(filename):
        print(f"⚠️  Файл не найден: {filename}")
        return False

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ищем nav с двумя ссылками
        old_nav = '''    <nav class="main-nav">
        <div class="container">
            <a href="../../../index.html">🏠 Главная</a>
            <a href="../act-2019.html">📋 Оглавление Акта 2019</a>
        </div>
    </nav>'''

        # Заменяем на nav с четырьмя ссылками
        new_nav = '''    <nav class="main-nav">
        <div class="container">
            <a href="../../../index.html">🏠 Главная</a>
            <a href="../act-2019.html">📋 Оглавление Акта 2019</a>
            <a href="../../../glossary.html">📖 Глоссарий</a>
            <a href="../../../references.html">🔍 Исторические справки</a>
        </div>
    </nav>'''

        if old_nav in content:
            content = content.replace(old_nav, new_nav)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Исправлен: {filename}")
            return True
        else:
            print(f"ℹ️  Навигация уже исправлена: {filename}")
            return True

    except Exception as e:
        print(f"❌ Ошибка {filename}: {e}")
        return False

def main():
    print("🔧 ДОБАВЛЕНИЕ ССЫЛОК В ШАПКУ СТАТЕЙ 37-45")
    print("=" * 60)

    fixed = 0
    for filename in files_to_fix:
        if fix_nav(filename):
            fixed += 1

    print()
    print(f"✅ Обработано файлов: {fixed}/{len(files_to_fix)}")

if __name__ == "__main__":
    main()
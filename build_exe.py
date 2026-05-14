#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
from pathlib import Path

MAIN_SCRIPT = Path(__file__).parent / "gif_splitter.py"

# Иконка‑новая: gif_icon_riya.ico
ICON_PATH = Path(__file__).parent / "icons" / "gif_icon_riya.ico"

ARGS = [
    "pyinstaller",
    "--onefile",                 # один exe‑файл
    "--windowed",                # GUI‑режим (без консоли)
    f"--icon={ICON_PATH}" if ICON_PATH.is_file() else "",
    "--name=GifSplitter",
    str(MAIN_SCRIPT),
]

# Убираем пустые элементы (если иконки нет)
ARGS = [a for a in ARGS if a]

print("Устанавливаем/обновляем PyInstaller …")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

print("Запускаем PyInstaller …")
subprocess.check_call(ARGS)

print("\n✅ Сборка завершена! exe‑файл находится в папке `dist/`")

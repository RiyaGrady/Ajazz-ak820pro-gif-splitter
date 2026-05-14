# build_exe.py (полный вариант)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from pathlib import Path

MAIN_SCRIPT = Path(__file__).parent / "gif_splitter.py"
ICON_PATH   = Path(__file__).parent / "icons" / "gif_icon_riya.ico"
SOUNDS_DIR  = Path(__file__).parent / "sounds"
EXE_PATH    = Path(__file__).parent / "dist" / "GifSplitter.exe"

# ----- Удаляем прежний exe, если он не запущен -----------------
if EXE_PATH.is_file():
    try:
        EXE_PATH.unlink()
    except PermissionError:
        sys.exit(
            "❌ Не удалось удалить старый GifSplitter.exe – файл, скорее всего, запущен.\n"
            "Закройте программу и запустите сборку снова."
        )

# ----- Формируем список аргументов -----------------------------
ARGS = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--clean",
    f"--icon={ICON_PATH}" if ICON_PATH.is_file() else "",
    "--name=GifSplitter",
    f"--add-data={SOUNDS_DIR}{os.pathsep}sounds",
    f"--add-data={ICON_PATH}{os.pathsep}icons" if ICON_PATH.is_file() else "",
    "--collect-all", "pillow",                # <‑‑ Ключевой момент
    "--hidden-import=PIL.PngImagePlugin",
    "--hidden-import=PIL.JpegImagePlugin",
    "--hidden-import=PIL.GifImagePlugin",
    str(MAIN_SCRIPT),
]

# удалить пустые элементы
ARGS = [a for a in ARGS if a]

print("🔧 Устанавливаем/обновляем PyInstaller …")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

print("🚀 Запуск PyInstaller …")
subprocess.check_call(ARGS)

print("\n✅ Сборка завершена! exe‑файл находится в папке `dist/`")

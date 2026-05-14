#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from tkinter import (
    Tk,
    Label,
    Button,
    filedialog,
    StringVar,
    messagebox,
)
from PIL import Image, ImageSequence
from tqdm import tqdm

# --------------------------------------------------------------
# Библиотека для воспроизведения звука (только Windows)
# --------------------------------------------------------------
try:
    import winsound
except Exception:      # если скрипт запустить на Linux/macOS
    winsound = None

# --------------------------------------------------------------
# Константы проекта
# --------------------------------------------------------------
DEFAULT_ROOT = Path(
    r"F:\Для экранчика клавитуры\Скрипт и папка для теста гивок\Исходные гифки"
).resolve()

# Папка со звуками (лежит рядом с этим скриптом)
SOUNDS_DIR = Path(__file__).parent / "sounds"
SUCCESS_SOUND = SOUNDS_DIR / "anime-wow.wav"
FAIL_SOUND    = SOUNDS_DIR / "split-sad-meow-song.wav"


# --------------------------------------------------------------
# Вспомогательная функция воспроизведения звука
# --------------------------------------------------------------
def _play(sound_path: Path):
    """Воспроизводит WAV‑файл, если он существует и winsound доступен."""
    if winsound and sound_path.is_file():
        winsound.PlaySound(str(sound_path), winsound.SND_ASYNC)


# --------------------------------------------------------------
# Работа с GIF‑файлом
# --------------------------------------------------------------
def resize_frame(frame: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Уменьшить кадр до указанного размера (LANCZOS)."""
    return frame.convert("RGBA").resize(size, Image.LANCZOS)


def split_gif(gif_path: Path, out_dir: Path, size: tuple[int, int] = (128, 128)):
    """Разбивает анимированный GIF, сохраняет кадры и возвращает out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(gif_path) as im:
        if not getattr(im, "is_animated", False):
            raise ValueError(f"{gif_path} не является анимированным GIF‑файлом")

        for i, frame in enumerate(
            tqdm(
                ImageSequence.Iterator(im),
                total=getattr(im, "n_frames", 1),
                desc="Обрабатываем кадры",
                leave=False,
            )
        ):
            resized = resize_frame(frame, size)
            out_path = out_dir / f"frame_{i:04d}.png"
            resized.save(out_path, format="PNG")

    # звук успеха
    _play(SUCCESS_SOUND)

    # --------------------------------------------------------------
    # 2️⃣ ОТКРЫТЬ ПАПКУ С РЕЗУЛЬТАТОМ (если ОС позволяет)
    # --------------------------------------------------------------
    try:
        # На Windows `os.startfile` открывает папку в Проводнике.
        # На macOS/Linux можно использовать `subprocess.run([...])`,
        # но в данном проекте ориентируемся на Windows.
        import os
        os.startfile(str(out_dir))
    except Exception as exc:          # если открытие не удалось – просто игнорируем
        # (можно добавить отладочный вывод, но приложение не падает)
        print(f"⚠️ Не удалось открыть папку автоматически: {exc}")

    return out_dir


# --------------------------------------------------------------
# CLI‑интерфейс
# --------------------------------------------------------------
def run_cli(cli_path: Path | None = None):
    """Запуск из терминала. Путь может быть передан как аргумент."""
    if cli_path is None:
        path = DEFAULT_ROOT
        print(f"⚙️ Путь по умолчанию: {path}")
    else:
        path = Path(cli_path).resolve()
        print(f"⚙️ Путь из аргумента: {path}")

    try:
        # ---------- определяем GIF ----------
        if path.is_dir():
            gif_files = list(path.glob("*.gif"))
            if not gif_files:
                raise FileNotFoundError(f"В папке {path} нет GIF‑файлов")
            gif_path = gif_files[0]
        else:
            gif_path = path

        out_dir = gif_path.parent / (gif_path.stem + "_frames")
        split_gif(gif_path, out_dir)
        print(f"✅ Кадры сохранены в «{out_dir}». Папка открыта в Проводнике (если это возможно).")
    except Exception as exc:
        _play(FAIL_SOUND)
        sys.exit(f"❌ Ошибка: {exc}")


# --------------------------------------------------------------
# GUI‑интерфейс (Tkinter)
# --------------------------------------------------------------
class GifSplitterGUI:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("GifSplitter")
        self.root.resizable(False, False)

        # Текущий путь (отображаем в окне)
        self.current_path = StringVar(value=str(DEFAULT_ROOT))

        Label(root, text="Текущий путь к GIF‑файлу (или папке):").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        Label(
            root,
            textvariable=self.current_path,
            wraplength=350,
            fg="blue",
        ).grid(row=1, column=0, padx=10, sticky="w")

        Button(
            root,
            text="Указать путь для вашего GIF‑файла",
            command=self._choose_path,
            width=30,
        ).grid(row=2, column=0, padx=10, pady=12)

    def _choose_path(self):
        """Открывает диалог, получает реальный путь к файлу и обрабатывает его."""
        chosen_file = filedialog.askopenfilename(
            title="Выберите GIF‑файл",
            filetypes=[("GIF files", "*.gif")],
        )
        if not chosen_file:            # пользователь нажал «Отмена»
            return

        # Обновляем отображаемый путь
        self.current_path.set(chosen_file)

        try:
            gif_path = Path(chosen_file).resolve()
            out_dir = gif_path.parent / (gif_path.stem + "_frames")
            split_gif(gif_path, out_dir)
            messagebox.showinfo(
                "Готово",
                f"Кадры успешно сохранены в папке:\n{out_dir}\n\nПапка была открыта автоматически.",
            )
        except Exception as exc:
            _play(FAIL_SOUND)
            messagebox.showerror(
                "Ошибка",
                f"Не удалось обработать файл:\n{exc}",
            )


def run_gui():
    root = Tk()
    GifSplitterGUI(root)
    root.mainloop()


# --------------------------------------------------------------
# Точка входа
# --------------------------------------------------------------
if __name__ == "__main__":
    # Если передан аргумент – работаем в CLI‑режиме, иначе открываем GUI
    if len(sys.argv) > 1:
        run_cli(sys.argv[1])
    else:
        run_gui()

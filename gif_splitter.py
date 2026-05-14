#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import os
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
# 1️⃣  Подготовка логирования
# --------------------------------------------------------------
def _init_logger() -> logging.Logger:
    """
    Создаёт и возвращает «корневой» logger.
    Файл журнала помещается в папку `logs/` рядом с исполняемым файлом.
    Формат имени: log_YYYYMMDD_HHMMSS.txt
    """
    # Вычисляем директорию, где будет храниться журнал
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Запуск из .exe – папка рядом с exe
        base_dir = Path(sys.executable).resolve().parent
    else:
        # Обычный запуск из исходников
        base_dir = Path(__file__).resolve().parent

    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logfile = logs_dir / f"log_{timestamp}.txt"

    # Формируем logger
    logger = logging.getLogger("GifSplitter")
    logger.setLevel(logging.DEBUG)          # захватываем всё, включая DEBUG

    # Формат сообщений
    fmt = "%(asctime)s | %(levelname)-8s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    # 1️⃣ Файловый хэндлер
    file_h = logging.FileHandler(logfile, encoding="utf-8")
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    logger.addHandler(file_h)

    # 2️⃣ Консольный хэндлер (stdout) – сохраняет совместимость с print‑ами
    console_h = logging.StreamHandler(sys.stdout)
    console_h.setLevel(logging.INFO)       # в консоль только INFO и выше
    console_h.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    logger.addHandler(console_h)

    logger.info(f"✅ Лог-файл создан: {logfile}")
    return logger


# Инициализируем сразу, чтобы далее использовать `logger`
from datetime import datetime
logger = _init_logger()

# --------------------------------------------------------------
# 2️⃣  Утилита для доступа к ресурсам (распакованным в exe)
# --------------------------------------------------------------
def _resource_path(relative: Path) -> Path:
    """
    Возвращает абсолютный путь к ресурсу как в «исходном» проекте,
    так и в упакованном exe (PyInstaller).
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)          # временная папка с данными
    else:
        base_path = Path(__file__).parent
    return base_path / relative


# --------------------------------------------------------------
# 3️⃣  Звук (только Windows)
# --------------------------------------------------------------
try:
    import winsound
except Exception:          # Linux/macOS
    winsound = None


# --------------------------------------------------------------
# 4️⃣  Константы проекта
# --------------------------------------------------------------
DEFAULT_ROOT = Path(
    r"F:\Для экранчика клавитуры\Скрипт и папка для теста гивок\Исходные гифки"
).resolve()

SOUNDS_DIR = _resource_path(Path("sounds"))
SUCCESS_SOUND = SOUNDS_DIR / "anime-wow.wav"
FAIL_SOUND = SOUNDS_DIR / "split-sad-meow-song.wav"


# --------------------------------------------------------------
# 5️⃣  Воспроизведение звука
# --------------------------------------------------------------
def _play(sound_path: Path | None):
    """Воспроизводит WAV‑файл, если он существует и winsound доступен."""
    if not sound_path or not sound_path.is_file():
        logger.debug(f"⚙️ Звук не найден/не указан: {sound_path}")
        return
    if winsound:
        logger.debug(f"🔊 Воспроизведение звука: {sound_path}")
        winsound.PlaySound(str(sound_path), winsound.SND_ASYNC)


# --------------------------------------------------------------
# 6️⃣  Работа с GIF‑файлом
# --------------------------------------------------------------
def resize_frame(frame: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Уменьшить кадр до указанного размера (LANCZOS)."""
    return frame.convert("RGBA").resize(size, Image.LANCZOS)

def _is_gui_mode() -> bool:
    """Возвращает True, если приложение запущено без консоли (Tkinter‑GUI)."""
    return getattr(sys, "frozen", False) and not sys.stdout

def split_gif(gif_path: Path, out_dir: Path, size: tuple[int, int] = (128, 128)):
    """Разбивает анимированный GIF, сохраняет кадры и возвращает out_dir."""
    logger.info(f"🚀 Обрабатываем GIF: {gif_path}")
    out_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(gif_path) as im:
        if not getattr(im, "is_animated", False):
            raise ValueError(f"{gif_path} не является анимированным GIF‑файлом")

        use_tqdm = not _is_gui_mode()  # в GUI‑режиме ставим False

        for i, frame in enumerate(
            tqdm(
                ImageSequence.Iterator(im),
                total=getattr(im, "n_frames", 1),
                desc="Обрабатываем кадры",
                leave=False,
                disable=not use_tqdm,  # отключаем, если use_tqdm=False
                file=sys.stdout or sys.stderr,
            )
        ):
            resized = resize_frame(frame, size)
            out_path = out_dir / f"frame_{i:04d}.png"
            try:
                resized.save(out_path, format="PNG")
                logger.debug(f"✅ Сохранён кадр {out_path}")
            except Exception as e:
                logger.error(f"❌ Ошибка сохранения кадра {out_path}: {e}")
                raise

    _play(SUCCESS_SOUND)

    # --------------------------------------------------------------
    # 2️⃣ ОТКРЫТЬ ПАПКУ С РЕЗУЛЬТАТОМ (если ОС позволяет)
    # --------------------------------------------------------------
    try:
        import os
        os.startfile(str(out_dir))            # Windows‑специфично
        logger.info(f"📂 Открыт каталог: {out_dir}")
    except Exception as exc:
        logger.warning(f"⚠️ Не удалось открыть папку автоматически: {exc}")

    return out_dir


# --------------------------------------------------------------
# 7️⃣  CLI‑интерфейс
# --------------------------------------------------------------
def run_cli(cli_path: Path | None = None):
    """Запуск из терминала. Путь может быть передан как аргумент."""
    if cli_path is None:
        path = DEFAULT_ROOT
        logger.info(f"⚙️ Путь по умолчанию: {path}")
    else:
        path = Path(cli_path).resolve()
        logger.info(f"⚙️ Путь из аргумента: {path}")

    try:
        if path.is_dir():
            gif_files = list(path.glob("*.gif"))
            if not gif_files:
                raise FileNotFoundError(f"В папке {path} нет GIF‑файлов")
            gif_path = gif_files[0]
        else:
            gif_path = path

        out_dir = gif_path.parent / (gif_path.stem + "_frames")
        split_gif(gif_path, out_dir)

        logger.info(f"✅ Кадры сохранены в «{out_dir}». Папка открыта в Проводнике (если это возможно).")
        print(f"✅ Кадры сохранены в «{out_dir}». Папка открыта в Проводнике (если это возможно).")
    except Exception as exc:
        _play(FAIL_SOUND)
        logger.exception("❌ Ошибка во время выполнения CLI")
        sys.exit(f"❌ Ошибка: {exc}")


# --------------------------------------------------------------
# 8️⃣  GUI‑интерфейс (Tkinter)
# --------------------------------------------------------------
class GifSplitterGUI:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("GifSplitter")
        self.root.resizable(False, False)

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
            logger.info("⚪ Пользователь отменил выбор файла.")
            return

        self.current_path.set(chosen_file)
        logger.info(f"🗂 Пользователь выбрал файл: {chosen_file}")

        try:
            gif_path = Path(chosen_file).resolve()
            out_dir = gif_path.parent / (gif_path.stem + "_frames")
            split_gif(gif_path, out_dir)

            messagebox.showinfo(
                "Готово",
                f"Кадры успешно сохранены в папке:\n{out_dir}\n\nПапка была открыта автоматически.",
            )
            logger.info(f"✅ GUI‑операция завершена успешно, результаты в {out_dir}")
        except Exception as exc:
            _play(FAIL_SOUND)
            messagebox.showerror(
                "Ошибка",
                f"Не удалось обработать файл:\n{exc}",
            )
            logger.exception("❌ Ошибка при работе GUI")


def run_gui():
    root = Tk()
    GifSplitterGUI(root)
    root.mainloop()


# --------------------------------------------------------------
# 9️⃣  Точка входа
# --------------------------------------------------------------
if __name__ == "__main__":
    # Если передан аргумент – работаем в CLI‑режиме, иначе открываем GUI
    if len(sys.argv) > 1:
        run_cli(sys.argv[1])
    else:
        run_gui()

**Для обычных пользователей (русский)**  

У меня возникала ошибка импорта всех GIF‑файлов в программе **AJAZZ AK820Pro**. Хотя GIF‑файлы можно самостоятельно изменить до размера 128 × 128 px и разделить на кадры с помощью бесплатных онлайн‑сервисов, я создал утилиту, которая делает это одной кнопкой.  

1. Скачайте `GifSplitter.exe` из папки **dist**: https://github.com/RiyaGrady/Ajazz-ak820pro-gif-splitter/tree/main/dist  
2. Запустите файл и укажите путь к вашему GIF‑файлу.  
3. Программа автоматически изменит размер изображения до 128 × 128 px и разобьёт его на отдельные кадры.  

После этого в **AJAZZ AK820Pro** можно создать новый проект и указать папку, содержащую все полученные кадры.  



**For regular users (English)**  

I kept getting an import error for all GIF files in the **AJAZZ AK820Pro** software. While you can resize GIFs to 128 × 128 px and split them into frames using free online services, I built a tool that does it with a single click.  

1. Download `GifSplitter.exe` from the **dist** folder: https://github.com/RiyaGrady/Ajazz-ak820pro-gif-splitter/tree/main/dist  
2. Run the executable and specify the path to your GIF file.  
3. The program will automatically resize the image to 128 × 128 px and split it into individual frames.  

You can then create a new project in **AJAZZ AK820Pro** and point it to the folder containing all the generated frames.

----------------------------

# Ajazz-ak820pro-gif-splitter
GifSplitter – принимает анимированный GIF, уменьшает каждый кадр до 128 × 128 px, сохраняет кадры в отдельную папку и озвучивает результат (успех/ошибка). Поддерживает как графический интерфейс (Tkinter), так и запуск из консоли с указанием пути. Затем папка, содержащая извлеченные кадры, автоматически открывается в проводнике.

1. <img width="358" height="201" alt="image" src="https://github.com/user-attachments/assets/fa8a0878-e6d9-4016-a998-f662b1ae56e4" />

2. <img width="1308" height="435" alt="image" src="https://github.com/user-attachments/assets/a37fd6f6-2100-4751-b799-c84937ba9c35" />

3. <img width="1537" height="860" alt="image" src="https://github.com/user-attachments/assets/68471e74-003e-44a5-ae39-2c1ebcd1d815" />

4. <img width="2280" height="1246" alt="image" src="https://github.com/user-attachments/assets/c17e9d36-c9df-4415-8a88-83f05037de9d" />

---  

## `README.md` для GitHub  

```markdown
# GifSplitter

**GifSplitter** – простая Windows‑утилита, которая разбивает анимированный GIF‑файл на отдельные кадры, уменьшает каждый кадр до **128 × 128 px** и сохраняет их в подпапку рядом с оригиналом. После завершения воспроизводятся звуковые сигналы (успех – `anime-wow.wav`, ошибка – `split-sad-meow-song.wav`).  

Программа имеет два режима работы:

* **GUI** – нажмите кнопку *«Указать путь для вашего GIF‑файла»* и выберите файл. После обработки появится диалоговое окно с путём к папке‑результату и звуковой сигнал.
* **CLI** – удобен для скриптов и автоматизации:  
  ```bash
  GifSplitter.exe "C:\path\to\my.gif"
  ```

## Содержание репозитория

```
gif_splitter/
│
├─ gif_splitter.py          # основной скрипт (логика + CLI + GUI)
├─ requirements.txt        # зависимости
├─ build_exe.py            # сборка .exe через PyInstaller
├─ icons/
│   └─ gif_icon_riya.ico   # иконка exe‑файла
└─ sounds/
    ├─ anime-wow.wav       # короткая мелодия – успех
    └─ split-sad-meow-song.wav  # звук ошибки
```

## Установка и сборка

### 1. Клонирование репозитория, Создание виртуального окружения (рекомендовано), Установка зависимостей  
```bash
git clone https://github.com/yourname/gif_splitter.git
cd gif_splitter
```
```
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux (не нужен для сборки exe)
```
```bash
pip install -r requirements.txt
```

### 2. Сборка самодостаточного `.exe`  
```bash
python build_exe.py
```
После завершения в папке `dist/` появится `GifSplitter.exe` (иконка **gif_icon_riya.ico**).

## Как пользоваться

### GUI (рекомендовано для обычных пользователей)

1. Двойной клик по `GifSplitter.exe`.  
2. Нажмите **«Указать путь для вашего GIF‑файла»**.  
3. Выберите нужный GIF‑файл.  
4. После успешного разреза появится диалоговое окно с путём к папке‑результату и прозвучит короткая мелодия **anime‑wow.wav**, и папка с извлеченными кадрами откроется автоматически.  

### CLI (для автоматизации)

```bash
GifSplitter.exe "D:\MyGifs\animation.gif"
```
*Если указан каталог, будет обработан первый найденный файл `*.gif` в этой папке.*  
При ошибке (не GIF, повреждённый файл и т.п.) будет воспроизведён звук **split‑sad‑meow‑song.wav** и выведено сообщение в консоль, и ни одна папка не открывается.

## Требования
* Python 3.9+ для сборки (пользователю достаточно только готовый `exe`).

ENGLISH
---------------

```markdown
# GifSplitter

**GifSplitter** – a simple Windows utility that splits an animated GIF file into individual frames, resizes each frame to **128 × 128 px**, and saves them in a sub‑folder next to the original. Upon completion a sound is played (success – `anime-wow.wav`, error – `split-sad-meow-song.wav`). The folder containing the extracted frames is then **automatically opened** in Explorer.  

The program works in two modes:

* **GUI** – click the **«Указать путь для вашего GIF‑файла»** button, choose a file, and after processing a dialog appears with the path to the output folder together with a success sound.  
* **CLI** – convenient for scripts and automation:  
  ```bash
  GifSplitter.exe "C:\path\to\my.gif"
  ```

## Repository contents

```
gif_splitter/
│
├─ gif_splitter.py          # main script (logic + CLI + GUI)
├─ requirements.txt        # dependencies
├─ build_exe.py            # builds the .exe with PyInstaller
├─ icons/
│   └─ gif_icon_riya.ico   # exe icon
└─ sounds/
    ├─ anime-wow.wav       # short melody – success
    └─ split-sad-meow-song.wav  # error sound
```

## Installation & Build

### 1. Clone the repository, create a virtual environment (recommended), install dependencies  

```bash
git clone https://github.com/yourname/gif_splitter.git
cd gif_splitter
```

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux (not needed for exe build)
```

```bash
pip install -r requirements.txt
```

### 2. Build a standalone `.exe`  

```bash
python build_exe.py
```

When finished, the `dist/` folder will contain `GifSplitter.exe` (icon **gif_icon_riya.ico**).

## How to use

### GUI (recommended for regular users)

1. Double‑click `GifSplitter.exe`.  
2. Press **«Указать путь для вашего GIF‑файла»**.  
3. Select the desired GIF file.  
4. After a successful split a dialog shows the path to the result folder and the short melody **anime-wow.wav** is played, and the folder with the extracted frames is opened automatically.

### CLI (for automation)

```bash
GifSplitter.exe "D:\MyGifs\animation.gif"
```

*If a directory is supplied, the first `*.gif` file found in that folder will be processed.*  
On failure (non‑GIF, corrupted file, etc.) the sound **split-sad-meow-song.wav** is played and an error message is printed to the console, and no folder is opened.

## Requirements

* Python 3.9+ for building (end users only need the compiled `exe`).  

import json
import matplotlib.pyplot as plt
import random

# --- Задание 2: Чтение данных из JSON ---
try:
    with open('music.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Ошибка: Файл music.json не найден. Убедитесь, что он находится в той же папке, что и скрипт.")
except json.JSONDecodeError:
    print("Ошибка: Файл music.json содержит некорректный JSON.")
else:

    # --- Задание 3: Расчёт метрик ---
    total_listen_time_minutes = sum(item['duration_minutes'] * item['listens'] for item in data)

    total_hours = int(total_listen_time_minutes // 60)
    total_minutes_remainder = int(total_listen_time_minutes % 60)

    genre_counts = {}
    for item in data:
        genre = item['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + item['listens']
    top_genre = max(genre_counts, key=genre_counts.get)

    most_listened_track = max(data, key=lambda x: x['listens'])

    # --- Вывод результатов в консоль с переводом в часы ---
    print("--- Анализ статистики прослушиваний ---")
    print(f"1. Суммарное время прослушивания: {total_listen_time_minutes:.2f} мин -> {total_hours} ч {total_minutes_remainder} мин")
    print(f"2. Топ-жанр: {top_genre} (суммарно {genre_counts[top_genre]} прослушиваний)")
    print(f"3. Самый прослушиваемый трек: '{most_listened_track['track_name']}' от {most_listened_track['artist']} ({most_listened_track['listens']} прослушиваний)")


# --- Задание 4: Визуализация статистики с цветами ---
# Словарь для сопоставления жанров и их цветов в формате HEX (#RRGGBB)
genre_colors = {
    "Поп": "#FFD700",   # Золотой
    "Электронная": "#00FFFF", # Циан (бирюзовый)
    "Фолк": "#8B4513",  # Седельный (коричневый)
    "Рок": "#800000",   # Темно-красный (бордовый)
    "Блюз": "#4169E1"   # Королевский синий
}

def generate_random_color():
    return "#{:06X}".format(random.randint(0, 0xFFFFFF))

# --- График 1: Количество прослушиваний по жанрам (столбчатая диаграмма) ---
genres = list(genre_counts.keys())
counts = list(genre_counts.values())

colors_for_bars = [genre_colors.get(genre, generate_random_color()) for genre in genres]

plt.figure(figsize=(10, 6))
plt.bar(genres, counts, color=colors_for_bars)
plt.title('Количество прослушиваний по жанрам')
plt.xlabel('Жанр')
plt.ylabel('Количество прослушиваний')
plt.tight_layout() # Чтобы подписи влезли

# --- График 2: Топ-5 самых прослушиваемых треков (горизонтальная диаграмма с градиентом) ---
# 1. Сортируем треки по количеству прослушиваний (по убыванию) и берем топ-5
sorted_tracks = sorted(data, key=lambda x: x['listens'], reverse=True)[:5]

# 2. Инвертируем порядок списков, чтобы самое большое значение было наверху
tracks_names = [f"{t['track_name']} - {t['artist']}" for t in sorted_tracks][::-1]
tracks_counts = [t['listens'] for t in sorted_tracks][::-1]

import numpy as np
import matplotlib.colors as mcolors

num_tracks = len(tracks_counts)

# Базовые цвета для градиента
light_orange = '#FFB347' # Светло-оранжевый
dark_orange = '#8B4513'  # Темно-оранжевый (коричневый)

cmap = mcolors.LinearSegmentedColormap.from_list('orange_to_dark_orange', [light_orange, dark_orange])

colors_for_bars = cmap(np.linspace(0, 1, num_tracks))[::-1]

plt.figure(figsize=(10, 6))
plt.barh(tracks_names, tracks_counts, color=colors_for_bars)
plt.title('Топ-5 самых прослушиваемых треков')
plt.xlabel('Количество прослушиваний')
plt.tight_layout()

# Показать все графики
plt.show()
import requests
import customtkinter as ctk
from datetime import datetime
from tkinter import Canvas
from PIL import Image, ImageEnhance, ImageTk
import os
import sys


# Функция для получения пути к файлам (иконки, изображения) при сборке через PyInstaller
def resource_path(relative_path):
    try:
        # PyInstaller создает временный путь к файлам
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Ваш API-ключ от WeatherAPI
API_KEY = "249f1386b3a04dba97653827240609"
CITY = "Chisinau"  # Латинизированное название города
URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=2&lang=ru"


# Функция для получения данных о погоде
def get_weather():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Проверка на наличие ошибок
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None


# Функция для отображения погоды
def display_weather(data):
    if data:
        today = datetime.today().date()

        # Прогнозы для сегодня и завтра
        today_forecast = ""
        tomorrow_forecast = ""
        today_summary = data['forecast']['forecastday'][0]['day']['condition']['text']
        tomorrow_summary = data['forecast']['forecastday'][1]['day']['condition']['text']

        # Прогноз на сегодня
        for forecast in data['forecast']['forecastday'][0]['hour']:
            forecast_time = datetime.strptime(forecast['time'], '%Y-%m-%d %H:%M')
            if forecast_time.date() == today:
                today_forecast += (f"{forecast_time.strftime('%H:%M')}: "
                                   f"{forecast['condition']['text']}, "
                                   f"{forecast['temp_c']}°C\n")

        # Прогноз на завтра
        for forecast in data['forecast']['forecastday'][1]['hour']:
            forecast_time = datetime.strptime(forecast['time'], '%Y-%m-%d %H:%M')
            tomorrow_forecast += (f"{forecast_time.strftime('%H:%M')}: "
                                  f"{forecast['condition']['text']}, "
                                  f"{forecast['temp_c']}°C\n")

        # Обновляем метки с прогнозом
        day_label.configure(text=f"Сегодня:\n{today_forecast}")
        tomorrow_label.configure(text=f"Завтра:\n{tomorrow_forecast}")
        today_summary_label.configure(text=f"Сегодня: {today_summary}")
        tomorrow_summary_label.configure(text=f"Завтра: {tomorrow_summary}")
    else:
        day_label.configure(text="Ошибка при получении данных.")
        tomorrow_label.configure(text="Ошибка при получении данных.")


# Настройки Customtkinter
ctk.set_appearance_mode("System")  # Установить тему (Light/Dark/System)
ctk.set_default_color_theme("blue")  # Установить цветовую тему

# Создание окна
root = ctk.CTk()
root.title("Прогноз погоды")
root.geometry("800x600")  # Задаем размер окна
root.resizable(False, False)  # Блокировка изменения размера окна

# Создание холста для фона
canvas = Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Загрузка и затемнение фонового изображения
image_path = resource_path("Weather.png")
bg_image_pil = Image.open(image_path)
enhancer = ImageEnhance.Brightness(bg_image_pil)
bg_image_brightened = enhancer.enhance(1.1)  # Увеличение яркости на дополнительные 10%
bg_image_tk = ImageTk.PhotoImage(bg_image_brightened)

canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

# Создание пользовательского шрифта с использованием CTkFont
custom_font = ctk.CTkFont(family="Helvetica", size=12, weight="bold")  # Пример шрифта

# Цвет текста для светлой и тёмной темы
light_mode_text_color = "#FFA500"  # Ярко оранжевый
dark_mode_text_color = "green"

# Цвет фона текста в обоих режимах
light_mode_bg_color = "#3A5FCD"  # Тёмно-голубой цвет
dark_mode_bg_color = "transparent"  # Прозрачный фон в тёмной теме

# Метки для отображения погоды с тёмно-голубым фоном и скруглёнными углами
day_label = ctk.CTkLabel(root, text="Загрузка данных на сегодня...", justify="left", bg_color=light_mode_bg_color,
                         fg_color=light_mode_text_color, font=custom_font, corner_radius=15)
day_label.place(relx=0.05, rely=0.1)

tomorrow_label = ctk.CTkLabel(root, text="Загрузка данных на завтра...", justify="left", bg_color=light_mode_bg_color,
                              fg_color=light_mode_text_color, font=custom_font, corner_radius=15)
tomorrow_label.place(relx=0.55, rely=0.1)

# Краткое описание погоды с тёмно-голубым фоном и скруглёнными углами
today_summary_label = ctk.CTkLabel(root, text="Краткое описание на сегодня", justify="left",
                                   bg_color=light_mode_bg_color,
                                   fg_color=light_mode_text_color, font=custom_font, corner_radius=15)
today_summary_label.place(relx=0.05, rely=0.8)

tomorrow_summary_label = ctk.CTkLabel(root, text="Краткое описание на завтра", justify="left",
                                      bg_color=light_mode_bg_color,
                                      fg_color=light_mode_text_color, font=custom_font, corner_radius=15)
tomorrow_summary_label.place(relx=0.55, rely=0.8)


# Функция для переключения темы
def switch_theme():
    if ctk.get_appearance_mode() == "Light":
        ctk.set_appearance_mode("Dark")
        day_label.configure(bg_color=dark_mode_bg_color, fg_color=dark_mode_text_color)
        tomorrow_label.configure(bg_color=dark_mode_bg_color, fg_color=dark_mode_text_color)
        today_summary_label.configure(bg_color=dark_mode_bg_color, fg_color=dark_mode_text_color)
        tomorrow_summary_label.configure(bg_color=dark_mode_bg_color, fg_color=dark_mode_text_color)
    else:
        ctk.set_appearance_mode("Light")
        day_label.configure(bg_color=light_mode_bg_color, fg_color=light_mode_text_color)
        tomorrow_label.configure(bg_color=light_mode_bg_color, fg_color=light_mode_text_color)
        today_summary_label.configure(bg_color=light_mode_bg_color, fg_color=light_mode_text_color)
        tomorrow_summary_label.configure(bg_color=light_mode_bg_color, fg_color=light_mode_text_color)


# Кнопка для переключения темы с углами
theme_button = ctk.CTkButton(root, text="Переключить тему", command=switch_theme,
                             corner_radius=15)  # Скруглённые углы кнопки
theme_button.place(relx=0.75, rely=0.9)

# Получение данных и отображение в интерфейсе
weather_data = get_weather()
display_weather(weather_data)

root.mainloop()

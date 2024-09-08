from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import requests
from datetime import datetime

API_KEY = "249f1386b3a04dba97653827240609"
CITY = "Chisinau"
URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=2&lang=ru"

class WeatherApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        weather_data = self.get_weather()

        if weather_data:
            today_forecast = weather_data['forecast']['forecastday'][0]['day']['condition']['text']
            tomorrow_forecast = weather_data['forecast']['forecastday'][1]['day']['condition']['text']

            label_today = Label(text=f"Сегодня: {today_forecast}", font_size='20sp')
            label_tomorrow = Label(text=f"Завтра: {tomorrow_forecast}", font_size='20sp')

            layout.add_widget(label_today)
            layout.add_widget(label_tomorrow)
        else:
            layout.add_widget(Label(text="Ошибка получения данных"))

        return layout

    def get_weather(self):
        try:
            response = requests.get(URL)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

if __name__ == "__main__":
    WeatherApp().run()

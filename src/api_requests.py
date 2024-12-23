import requests
from config import API_KEY


def get_location_key(location):
    try:
        response = requests.get(
            "https://dataservice.accuweather.com/"
            "locations/v1/cities/translate.json",
            params={
                "apikey": API_KEY,
                "q": location.lower(),
                "language": "ru-ru",
                "details": "true",
            },
        )
        response.raise_for_status()
        data = response.json()
        if response.status_code == 200 and data:
            return data[0]["Key"]
        else:
            print("Не удалось получить ключ местоположения.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении местоположения: {e}")
        return None


def get_weather_by_location(location, days=5):
    try:
        location_key = get_location_key(location)
        if location_key is None:
            return "Ошибка: Не удалось получить ключ местоположения."

        response = requests.get(
            "https://dataservice.accuweather.com/"
            f"forecasts/v1/daily/{5 if days > 1 else 1}day/{location_key}",
            params={
                "apikey": API_KEY,
                "language": "ru-ru",
                "details": "true",
                "metric": "true",
            },
        )
        response.raise_for_status()

        data = response.json()
        forecast_message = ""

        for day in data["DailyForecasts"][:days]:
            date = day["Date"]
            max_temp = day["Temperature"]["Maximum"]["Value"]
            min_temp = day["Temperature"]["Minimum"]["Value"]
            humidity = day["Day"]["RelativeHumidity"]["Average"]
            wind_speed = day["Day"]["Wind"]["Speed"]["Value"]
            rain_probability = day["Day"]["RainProbability"]
            weather_description = day["Day"]["LongPhrase"]

            forecast_message += (
                f"📅 <b>Дата:</b> {date}\n"
                f"🌡️ <b>Максимальная температура:</b> {max_temp}°C\n"
                f"🌡️ <b>Минимальная температура:</b> {min_temp}°C\n"
                f"💧 <b>Влажность:</b> {humidity}%\n"
                f"💨 <b>Скорость ветра:</b> {wind_speed} км/ч\n"
                f"🌧️ <b>Вероятность дождя:</b> {rain_probability}%\n"
                f"📝 <b>Описание:</b> {weather_description}\n\n"
            )

        return forecast_message

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении погоды: {e}")
        return {"error": str(e)}


def get_weather_info(data, interval, get_cached=False):
    if get_cached:
        with open("saved_answers/answer.txt", "r", encoding="utf-8") as file:
            return file.read()

    route = []
    route += [data["start_point"]]
    route += data["intermediate_points"]
    route += [data["end_point"]]

    answer = "\n"
    for point in route:
        answer += f"🌤 <b>Местоположение:</b> {point}\n\n"

        try:
            weather_info = get_weather_by_location(point, interval)
            if isinstance(weather_info, str):
                answer += weather_info
            else:
                answer += "Ошибка при получении погоды\n\n"
        except Exception as e:
            answer += f"Ошибка: {str(e).replace(API_KEY, '<API_KEY>')}"

    return answer


def main():
    print(get_weather_info(
        {
            "start_point": "Москва",
            "end_point": "Санкт-Петербург",
            "intermediate_points": [],
        },
        5,
    )
    )


if __name__ == "__main__":
    main()

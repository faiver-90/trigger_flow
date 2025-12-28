from typing import Any

import httpx

BASE_URL = "https://api.openweathermap.org"


class OpenWeatherService:
    """
    Клиент для работы с OpenWeatherMap API.
    Поддерживает: текущую погоду, 5-дневный прогноз, One Call 3.0 и геокодинг.
    """

    def __init__(self, api_key: str):
        """
        Args:
            api_key (str): Ваш API-ключ от OpenWeatherMap.
        """
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_current_weather(
        self,
        city: str | None = None,
        lat: float | None = None,
        lon: float | None = None,
        units: str = "metric",
        lang: str = "en",
    ) -> dict[str, Any]:
        """
        Получить текущую погоду.

        Аргументы могут быть:
        - city (например, "London,GB")
        - lat + lon

        Опциональные:
        - units: standard/metric/imperial
        - lang: "en", "ru" и т.д.

        Возвращает:
            JSON с текущей погодой.
        """
        params = {"appid": self.api_key, "units": units, "lang": lang}
        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"], params["lon"] = lat, lon
        else:
            raise ValueError("Нужно указать city или lat+lon или zip_code")

        resp = await self.client.get(f"{BASE_URL}/data/2.5/weather", params=params)
        resp.raise_for_status()
        return resp.json()

    async def geocoding_reverse(
        self,
        lat: float,
        lon: float,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Обратное геокодирование — по координатам возвращает названия городов.
        """
        resp = await self.client.get(
            f"{BASE_URL}/geo/1.0/reverse",
            params={"lat": lat, "lon": lon, "limit": limit, "appid": self.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        """Закрыть HTTP-клиент."""
        await self.client.aclose()

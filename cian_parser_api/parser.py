from .config import HEADERS, CIAN_API_URL, SEARCH_PAYLOAD
import httpx
from typing import Optional, List
from datetime import datetime, timedelta

class CianParser: 
    """Класс парсера объявлений Циан"""

    def __init__(self): 
        self.headers = HEADERS
        self.api_url = CIAN_API_URL
        self.payload = SEARCH_PAYLOAD

    async def fetch_listings(self) -> List[dict]:
        """
        Получение списка объявлений с Циан
        
        Returns:
            List[dict]: Список объявлений
        """
        # Создаем сессию для сохранения cookies между запросами
        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True,
            cookies={}
        ) as session:
            # Шаг 1: GET запрос на главную страницу для получения cookies
            print("1. Получаем cookies с главной страницы...")
            response = await session.get("https://www.cian.ru/")
            print(f"   Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Ошибка при получении главной страницы")
                print(f"   Response: {response.text[:500]}")
                raise Exception(f"Не удалось получить главную страницу: {response.status_code}")
            
            # Шаг 2: POST запрос к API с правильным Referer
            print("2. Делаем API запрос...")
            
            # Обновляем заголовки для API запроса - важен правильный Referer
            api_headers = self.headers.copy()
            api_headers["Referer"] = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&max_commission=0&offer_type=flat&region=1&sort=creation_date_desc"
            
            response = await session.post(
                self.api_url,
                json=self.payload,
                headers=api_headers
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Cookies: {dict(session.cookies)}")
            
            if response.status_code != 200:
                print(f"   Ошибка API запроса")
                print(f"   Response: {response.text[:1000]}")
                raise Exception(f"API вернул ошибку: {response.status_code}")
            
            # Парсим JSON
            data = response.json()
            print(f"3. Парсим JSON ответ...")
            offers = data.get('data', {}).get('offersSerialized', [])
            print(f"   Найдено объявлений: {len(offers)}")
            
            return offers

    def parse_offer(self, offer: dict) -> dict:
        """
        Парсинг одного объявления
        
        Args:
            offer: JSON данные объявления
            
        Returns:
            dict: Данные объявления
        """
        is_early_access = offer.get('isEarlyAccessEnabled', False)
        added_timestamp = offer.get('addedTimestamp')
        phone_reveal_at = None

        if is_early_access and added_timestamp:
            phone_reveal_at = datetime.fromtimestamp(added_timestamp) + timedelta(hours=3)
        
        # Вспомогательная функция для безопасного преобразования в int
        def safe_int(value, default=0):
            if value is None:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return default
        
        return {
            # ID и URL
            'cian_id': offer.get('cianId'),
            'external_url': offer.get('fullUrl'),
                    
            # Квартира
            'price': safe_int(offer.get('bargainTerms', {}).get('price', 0)),
            'rooms_count': offer.get('roomsCount') or 0,
            'area': safe_int(offer.get('totalArea', 0)),  #Квадратура
            'floor': offer.get('floorNumber') or 0,  #Этаж
            'floors_count': offer.get('building', {}).get('floorsCount', 0) or 0,  #Всего этажей

            # Локация
            'city': offer.get('geo', {}).get('address', [{}])[0].get('name', 'Москва'),
            'metro_station': self._get_first_metro(offer),
            'address': offer.get('geo', {}).get('userInput', ''),
            'coordinates_lat': offer.get('geo', {}).get('coordinates', {}).get('lat'),
            'coordinates_lng': offer.get('geo', {}).get('coordinates', {}).get('lng'),

            # Владелец и телефон
            'owner_id': offer.get('cianUserId'),
            'phone_number': self._get_phone_number(offer),

            #Время
            'created_at': self._parse_datetime(offer.get('creationDate')),
            'published_at': self._parse_timestamp(added_timestamp),

            # Ранний доступ
            'is_early_access': is_early_access,
            'phone_reveal_at': phone_reveal_at,

            # Дополнительная информация
            'description': offer.get('description'),
            'is_by_homeowner': offer.get('isByHomeowner'),
            'status': offer.get('status'),
            'photos': [photo.get('fullUrl') for photo in offer.get('photos', [])],

            }

    def _get_first_metro(self, offer: dict) -> Optional[str]:
        """Полууение первой станции метро"""
        undergrounds = offer.get('geo', {}).get('undergrounds', [])
        return undergrounds[0].get('name') if len(undergrounds) > 0 else None

    def _get_phone_number(self, offer:dict) -> Optional[str]:
        """Получение номера телефона"""
        phones = offer.get('phones', [])
        if len(phones) > 0:
            country_code = phones[0].get('countryCode', '')
            number = phones[0].get('number', '')
            return f'+{country_code}{number}'
        return ''
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """парсинг ISO datetime строки"""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                pass
        return None
    
    def _parse_timestamp(self, timestamp: Optional[int]) -> Optional[datetime]:
        """Прсинг Unix timestamp"""
        if timestamp:
            try:
                return datetime.fromtimestamp(timestamp)
            except:
                pass
        return None


async def main():
    """Главная функция для запуска парсера"""
    parser = CianParser()
    
    print("Запрос к API Циан...")
    
    try:
        # Получение списка объявлений
        offers = await parser.fetch_listings()
        
        print(f"\nНайдено объявлений: {len(offers)}\n")
        
        # Парсинг каждого объявления
        listings = []
        for i, offer in enumerate(offers, 1):
            listing = parser.parse_offer(offer)
            listings.append(listing)
            
            # Вывод в консоль
            print(f"--- Объявление {i} ---")
            print(f"  ID: {listing['cian_id']}")
            print(f"Ссылка: {listing['external_url']}")
            print(f"  Комнаты: {listing['rooms_count']}")
            print(f"  Площадь: {listing['area']} м²")
            print(f"  Этаж: {listing['floor']}/{listing['floors_count']}")
            print(f"  Адрес: {listing['address']}")
            print(f"  Метро: {listing['metro_station']}")
            print(f"  Цена: {listing['price']} ₽")
            print(f"  Телефон: {listing['phone_number'] or 'Не доступен'}")
            print(f"  Ранний доступ: {'Да' if listing['is_early_access'] else 'Нет'}")
            if listing['phone_reveal_at']:
                print(f"  Телефон будет доступен: {listing['phone_reveal_at']}")
            print()
        
        print(f"{'='*60}")
        print(f"Всего распарсено: {len(listings)}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
from datetime import datetime, timedelta
from typing import Optional


def map_offer(offer: dict) -> dict:
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
        
        return {
            # ID и URL
            'cian_id': offer.get('cianId'),
            'source': 'cian',
            'external_url': offer.get('fullUrl'),
                    
            # Квартира
            'price': _safe_int(offer.get('bargainTerms', {}).get('price', 0)),
            'rooms_count': offer.get('roomsCount') or 0,
            'area': _safe_int(offer.get('totalArea', 0)),  #Квадратура
            'floor': offer.get('floorNumber') or 0,  #Этаж
            'floors_count': offer.get('building', {}).get('floorsCount', 0) or 0,  #Всего этажей

            # Локация
            'city': offer.get('geo', {}).get('address', [{}])[0].get('name', 'Москва'),
            'metro_station': _get_first_metro(offer),
            'address': offer.get('geo', {}).get('userInput', ''),
            'coordinates_lat': offer.get('geo', {}).get('coordinates', {}).get('lat'),
            'coordinates_lng': offer.get('geo', {}).get('coordinates', {}).get('lng'),

            # Владелец и телефон
            'owner_id': offer.get('cianUserId'),
            'phone_number': _get_phone_number(offer),

            #Время
            'created_at': _parse_datetime(offer.get('creationDate')),
            'published_at': _parse_timestamp(added_timestamp),

            # Ранний доступ
            'is_early_access': is_early_access,
            'phone_reveal_at': phone_reveal_at,

            # Дополнительная информация
            'description': offer.get('description'),
            'is_by_homeowner': offer.get('isByHomeowner'),
            'status': offer.get('status'),
            'photos': [photo.get('fullUrl') for photo in offer.get('photos', [])],

            }
# Вспомогательная функция для безопасного преобразования в int
def _safe_int(value, default=0):
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default
        
def _get_first_metro(offer: dict) -> Optional[str]:
    """Полууение первой станции метро"""
    undergrounds = offer.get('geo', {}).get('undergrounds', [])
    return undergrounds[0].get('name') if len(undergrounds) > 0 else None

def _get_phone_number(offer:dict) -> Optional[str]:
    """Получение номера телефона"""
    phones = offer.get('phones', [])
    if len(phones) > 0:
        country_code = phones[0].get('countryCode', '')
        number = phones[0].get('number', '')
        return f'+{country_code}{number}'
    return ''
    
def _parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """парсинг ISO datetime строки"""
    if date_str:
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            pass
    return None
    
def _parse_timestamp(timestamp: Optional[int]) -> Optional[datetime]:
    """Прсинг Unix timestamp"""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp)
        except:
            pass
    return None
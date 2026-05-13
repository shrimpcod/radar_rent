# cian_parser/config.py
# URL для получения данных о квартирах с Циан
CIAN_SEARCH_URL = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&max_commission=0&offer_type=flat&region=1&sort=creation_date_desc"

CIAN_API_URL = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"

# Заголовки для запроса (чтобы выглядеть как обычный браузер)
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     # "Accept-Encoding": "gzip, deflate, br",  # Убираем чтобы избежать проблем с декодированием
#     "Connection": "keep-alive",
#     "Referer": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&max_commission=0&offer_type=flat&region=1&sort=creation_date_desc",
#     "Origin": "https://www.cian.ru",
#     "Content-Type": "application/json",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Ch-Ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "Windows",
# }

SEARCH_PAYLOAD = {
    "jsonQuery": {
    "_type": "flatrent",
    "sort": {
      "type": "term",
      "value": "creation_date_desc"
    },
    "engine_version": {
      "type": "term",
      "value": 2
    },
    "region": {
      "type": "terms",
      "value": [1]
    },
    "is_by_homeowner": {
      "type": "term",
      "value": "true"
    },
    "bbox": {
      "type": "term",
      "value": [
        [35.927444268, 54.910057939],
        [38.8882596977, 56.3045104224]
      ]
    },
    "for_day": {
      "type": "term",
      "value": "!1"
    },
    "commission": {
      "type": "range",
      "value": {
        "lte": 0
      }
    }
  }
} 


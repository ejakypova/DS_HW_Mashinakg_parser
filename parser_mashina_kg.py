import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin

"""1. Создать requests.Session с заголовками браузера"""
"""2. Загрузить страницу 1 → https://mashina.kg/search/passenger"""
"""3. Через BeautifulSoup найти все <a href="/details/..."> → распарсить карточки"""
"""4. Найти кнопки .pagination_button → определить общее число страниц"""
"""5. Для каждой следующей страницы (?page=2, ?page=3, ...):
   a. Подождать DELAY_SECONDS
   b. Загрузить HTML
   c. Распарсить карточки
   d. Добавить новые объявления (дедупликация по url)"""
"""6. Сохранить все данные в CSV через pandas"""

#============================Настройки========================================================

BASE_URL = "https://mashina.kg/search/passenger" # Базовая URL(ссылка) на сайт который мы парсим
OUTPUT_CSV = 'mashina_kg.csv' # название файла куда мы запишем наши данные
DELAY_SECONDS = 1.5 # Пауза между запросами, во избежения Ddos атак и получить бан или ошибку 429
PAGE_TO_PARSE = None # Сколько страниц нам нажо обработать
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}

# ======================1. Создать requests.Session с заголовками браузера=============================
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
"""
requests.Session() - переиспользует TCP - соединение и cookies (кеш) между запросами
для чего это нам:
1. Ускоряет работу(не создаем новую ссесию каждый раз)(то не открываем новый браузер)
2. автоматический сохраняет cookies, которые ставит при первом входе на сайт.
3. бывают моменты когда cookies не приняты выкидывается ошибка 403

"""
"""
def get_html(url: str, retries: int = 3) -> str | None:
    
    for attempt in range(1, retries+1):
        try:
            response = SESSION.get(url, timeout=15)
            #timeout=15 - не ждем дольше чем 15 секунд
            response.raise_for_status()
            # Если сервер вернул нам 4хх или 5хх ошибку - вызовется исключение
            return response.text
        except requests.RequestException as e:
            print(f"Попытка {attempt}/{retries} для {url}: {e}")
            
            # Если сервер не отвечает и это наша последняя попытка то мы сдаемся
            if attempt == retries:
                return None
            
            time.sleep(2 ** attempt)
            # Экспонциональная пауза: 2c, 4c, 9c -даем серверу остыть и смешиваемся с другими запросами
    return None

print(get_html(url=BASE_URL))"""

def get_html(session: requests.Session, url: str) -> str | None:
    """
    Загружает HTML страницы.
    """

    try:
        response = session.get(url, timeout=30)

        if response.status_code != 200:
            print(f"[ERROR] {url} -> статус {response.status_code}")
            return None

        return response.text

    except Exception as e:
        print(f"[EXCEPTION] {url} -> {e}")
        return None


# ==================== Вспомогательные функции для очистки ===============================
def extract_price(text: str) -> int | None:
    """
    Превращает строку с ценой в число
    для очистки цены "1432123 сом" -> 1432123
    
    Алгорит работы:
    1) Если в тексте есть слово 'сом' берем цифры, которые идут Непосредственно до него(перед ним) 
        с возможными пробелами между ними
        Это защищает нас от того что в тексте не будет год, обьем
    2) если 'сом' нет берем все цифры подряд
    """
    if not text:
        return None
    
    text = text.replace("\xa0", ' ')
    #Нормализовали неразрывные пробелы (\xa0) в обычные
    
    match = re.search(r'([\d\s]+)\s*сом', text)
    # Ищем цифры [пробелы цифры] ... сом
    if match:
        digits = re.sub(r'\D', '', match.group(1))
        return int(digits) if digits else None
    
    digits = re.sub(r'\D', '', text)
    return int(digits) if digits else None

def extract_year(text: str) -> int | None:
    """
    Достает год из строк
    берем 4 значное число в диапазоне 1900-2099
    """
    if not text:
        return None
    
    match =re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return int(match.group(1)) if match else None

def extract_mileage(text: str) -> int | None:
    
    if not text:
        return None
    
    digits = re.sub(r'[^\d]', "", text)
    return int(digits) if digits else None

# ===================Получение количества страниц ==============================

def get_total_pages(soup: BeautifulSoup) -> int:

    pages = []

    buttons = soup.select("button.pagination_button")

    for btn in buttons:
        text = btn.get_text(strip=True)

        if text.isdigit():
            pages.append(int(text))

    if not pages:
        return 1

    return max(pages)  
    
#=================3. Через BeautifulSoup найти все <a href="/details/..."> → распарсить карточки=====

def parce_cartochka(card) -> dict | None:
    """
    Парсит одну карточку автомобиля.
    """

    try:

        # ===================== URL =====================

        href = card.get("href", "")

        if not href.startswith("/details/"):
            return None

        full_url = urljoin(BASE_URL, href)

        # ===================== TITLE =====================

        title_tag = card.find("h3")

        title = (
            title_tag.get_text(strip=True)
            if title_tag
            else None
        )

        # ===================== IMAGE =====================

        img_tag = card.find("img")

        image_url = (
            img_tag.get("src")
            if img_tag
            else None
        )

        # ===================== CITY =====================

        city = None

        city_tag = card.find(
            "span",
            class_="text-white text-sm leading-5 truncate"
        )

        if city_tag:
            city = city_tag.get_text(strip=True)

        # ===================== YEAR / MILEAGE =====================

        year = None
        mileage_km = None

        spans = card.find_all("span")

        for span in spans:

            text = span.get_text(" ", strip=True)

            if re.search(r"\d{4}\s*/\s*\d+", text):

                parts = text.split("/")

                if len(parts) == 2:

                    year = re.sub(r"\D", "", parts[0])

                    mileage_km = re.sub(r"\D", "", parts[1])

                break

        # ===================== PRICE USD =====================

        price_usd = None

        for span in spans:

            text = span.get_text(" ", strip=True)

            if "$" in text:

                price_usd = re.sub(r"[^\d]", "", text)
                break

        # ===================== PRICE KGS =====================

        price_kgs = None

        kgs_tag = card.find(
            "span",
            class_="font-bold text-xs leading-4 text-text-secondary whitespace-nowrap"
        )

        if kgs_tag:

            price_kgs = re.sub(
                r"[^\d]",
                "",
                kgs_tag.get_text(strip=True)
            )

        # ===================== ENGINE / TRANSMISSION =====================

        engine = None
        transmission = None

        for span in spans:

            text = span.get_text(" ", strip=True)

            if "л." in text and "/" in text:

                parts = text.split("/")

                if len(parts) == 2:

                    engine = parts[0].strip()
                    transmission = parts[1].strip()

                break

        return {
            "url": full_url,
            "title": title,
            "price_usd": price_usd,
            "price_kgs": price_kgs,
            "year": year,
            "mileage_km": mileage_km,
            "engine": engine,
            "transmission": transmission,
            "city": city,
            "image_url": image_url,
        }

    except Exception as e:
        print(f"[CARD ERROR] {e}")
        return None

# ========================= ПАРСИНГ СТРАНИЦЫ =========================

def parse_page(html: str) -> list[dict]:
    """
    Парсит HTML страницы и
    возвращает список автомобилей.
    """

    soup = BeautifulSoup(html, "lxml")

    cars = []

    # Все ссылки на карточки
    cards = soup.select('a[href^="/details/"]')

    for card in cards:

        parsed = parce_cartochka(card)

        if parsed:
            cars.append(parsed)

    return cars


# ========================= СБОР ВСЕХ СТРАНИЦ =========================

def fetch_all_pages(session: requests.Session) -> list[dict]:
    """
    Перебирает страницы и
    собирает объявления.
    """

    all_cars = []

    seen_urls = set()

    # ===================== СТРАНИЦА 1 =====================

    print("[INFO] Загружаем страницу 1...")

    html = get_html(session, BASE_URL)

    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")

    total_pages = get_total_pages(soup)

    print(f"[INFO] Всего страниц: {total_pages}")

    if PAGE_TO_PARSE:
        total_pages = min(total_pages, PAGE_TO_PARSE)

    # ===================== ОБХОД СТРАНИЦ =====================

    for page in range(1, total_pages + 1):

        if page == 1:
            page_url = BASE_URL
        else:
            page_url = f"{BASE_URL}?page={page}"

        print(f"\n[PAGE] {page}/{total_pages}")

        if page != 1:
            time.sleep(DELAY_SECONDS)

            html = get_html(session, page_url)

            if not html:
                continue

        cars = parse_page(html)

        added = 0

        for car in cars:

            if car["url"] not in seen_urls:

                seen_urls.add(car["url"])
                all_cars.append(car)

                added += 1

        print(
            f"[INFO] Найдено: {len(cars)} | "
            f"Добавлено новых: {added} | "
            f"Всего: {len(all_cars)}"
        )

    return all_cars


# ========================= СОХРАНЕНИЕ CSV =========================

def save_to_csv(data: list[dict], filename: str):

    df = pd.DataFrame(data)

    df.to_csv(
        filename,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\n[SAVED] Данные сохранены в {filename}")


# ========================= MAIN =========================

def main():

    session = requests.Session()
    session.headers.update(HEADERS)

    cars = fetch_all_pages(session)

    if not cars:
        print("[INFO] Данные не получены")
        return

    save_to_csv(cars, OUTPUT_CSV)


if __name__ == "__main__":
    main()
    
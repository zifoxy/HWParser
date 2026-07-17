from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup


def get_cny_rate(day: date) -> tuple[str, str] | None:
    """Возвращает (дата курса ЦБ, значение) для юаня на указанный день."""
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={day.strftime('%d/%m/%Y')}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    cny = soup.find("CharCode", string="CNY")
    if cny is None:
        return None

    valute = cny.parent
    value = valute.find("Value").text
    rate_date = soup.find("ValCurs")["Date"]
    return rate_date, value


start = date(2025, 1, 10)
end = date(2025, 1, 20)

print("Курс китайского юаня (CNY) по данным ЦБ РФ")
print(f"Период: {start.strftime('%d.%m.%Y')} — {end.strftime('%d.%m.%Y')}")
print("-" * 40)

current = start
while current <= end:
    result = get_cny_rate(current)
    if result is None:
        print(f"{current.strftime('%d.%m.%Y')}: курс не найден")
    else:
        rate_date, value = result
        print(f"{current.strftime('%d.%m.%Y')}: {value} руб. (курс ЦБ на {rate_date})")
    current += timedelta(days=1)

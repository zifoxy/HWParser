from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup


def parse_date(text: str) -> date:
    return datetime.strptime(text.strip(), "%d.%m.%Y").date()


def get_dates() -> list[date]:
    today = date.today()
    print(f"Введите период (формат ДД.ММ.ГГГГ, не позже {today.strftime('%d.%m.%Y')})")

    while True:
        try:
            start = parse_date(input("Дата начала: "))
            end = parse_date(input("Дата конца: "))
        except ValueError:
            print("Неверный формат. Пример: 10.01.2025")
            continue

        if start > today or end > today:
            print(f"Дата не может быть позже {today.strftime('%d.%m.%Y')}")
            continue
        if start > end:
            print("Дата начала не может быть позже даты конца")
            continue

        dates = []
        current = start
        while current <= end:
            dates.append(current)
            current += timedelta(days=1)
        return dates


def get_cny_rate(day: date) -> tuple[str, str] | None:
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


dates = get_dates()

print("\nКурс китайского юаня (CNY) по данным ЦБ РФ")
print(f"Период: {dates[0].strftime('%d.%m.%Y')} — {dates[-1].strftime('%d.%m.%Y')}")
print("-" * 40)

for current in dates:
    result = get_cny_rate(current)
    if result is None:
        print(f"{current.strftime('%d.%m.%Y')}: курс не найден")
    else:
        rate_date, value = result
        print(f"{current.strftime('%d.%m.%Y')}: {value} руб. (курс ЦБ на {rate_date})")

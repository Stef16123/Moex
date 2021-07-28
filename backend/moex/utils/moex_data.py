import asyncio
from moex.models import Price
from scripts.main import get_history_price


def pull_price(security, start, end):
    data = asyncio.run(get_history_price(security.code, start, end))
    batch = [Price(date=price['TRADEDATE'], price=price['CLOSE'], security=security) for price in data]
    Price.objects.bulk_create(batch)

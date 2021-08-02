import asyncio
import aiohttp
import aiomoex
from moex.models import Price, Security
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def __init__(self):
        self.args = ['code', 'start', 'end']

    def add_arguments(self, parser):
        for arg in self.args:
            parser.add_argument(arg)

    def handle(self, **options):
        code = options['code']
        start = options['start']
        end = options['end']

        async def get_history_price(code, start, end):
            price_columns = ['SECID', 'CLOSE', 'TRADEDATE']
            session = aiohttp.ClientSession()
            history_price = await aiomoex.get_market_history(session, code,
                                                             columns=price_columns, start=start, end=end)
            await session.close()
            return history_price

        data = asyncio.run(get_history_price(code, start, end))
        security = Security.objects.get(code=code)
        batch = [Price(date=price['TRADEDATE'], price=price['CLOSE'], security=security) for price in data]
        Price.objects.bulk_create(batch)
        print('prices added in database')

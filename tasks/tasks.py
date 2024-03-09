import asyncio

from celery import Celery

from config import REDIS_URL, bot
from database.orm import database
from services import WBService

wb = WBService()

app = Celery('app', broker=REDIS_URL)
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'run-every-five-minutes': {
        'task': 'tasks.tasks.mailing_task',
        'schedule': 300.0
    },
}


async def start_mailing():
    mailings = await database.get_all_mailings()
    for mailing in mailings:
        msg, _ = await wb.get_product(mailing.product_id)
        await bot.send_message(mailing.user_id, msg)
        await asyncio.sleep(0.5)


celery_event_loop = asyncio.new_event_loop()


@app.task
def mailing_task():
    celery_event_loop.run_until_complete(start_mailing())

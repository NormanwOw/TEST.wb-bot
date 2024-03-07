import asyncio

from config import bot, dp
from handlers.user_handlers import router as user_router


dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError:
        quit()


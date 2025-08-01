import asyncio
from telegram import Bot
import time

class TelegramNotifier:
    def __init__(self, token: str, chat_id: int):
        self.bot = Bot(token=token)
        self.chat_id = 5610343610

    async def _send(self, message: str):
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    def send_message(self, message: str):
        try:
            asyncio.run(self._send(message))
            print("Telegram alert sent successfully.")
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

    def send_messages(self, messages, delay=1.0):
        """
        Send messages sequentially with delay to avoid connection pool issues.
        """
        for msg in messages:
            self.send_message(msg)
            time.sleep(delay)

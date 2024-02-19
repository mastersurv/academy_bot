from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext



async def start_handler(self, message: Message, state: FSMContext):
    tg_id = message.from_user.id
    text = message.text[7:]

    start_text = await self.db.get_start_text(bot_token=self.bot_token)

    await self.bot.send_message(
        chat_id=tg_id,
        text=start_text

    )

    if text == ""
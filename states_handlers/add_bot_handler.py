from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from utils.functions.get_bot_and_db import get_bot_and_db
from blanks.bot_markup import menu


async def add_bot_state(self, message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    text = message.text
    tg_id = message.from_user.id
    mess_id = message.message_id

    if text[:10].isdigit() and text[10] == ":":
        # loading_message = await self.bot.send_message(
        #     chat_id=tg_id,
        #     text=loading_text
        # )

        try:
            tokens = self.db.get_tokens()

            if tokens is None or text not in tokens:
                db.add_bot(
                    tg_id=tg_id,
                    bot_token=text
                )

                # self.db.start_message(
                #     method="save",
                #     bot_token=text,
                #     text="Стартовое сообщение"
                # )
                #
                # self.funnel_db.add_funnel(
                #     token=text,
                #     tg_id=tg_id
                # )

                async with state.proxy() as data:
                    try:
                        await self.bot.delete_message(
                            chat_id=tg_id,
                            message_id=data["message_id"]
                        )
                    except Exception:
                        pass

                    try:
                        await self.bot.delete_message(
                            chat_id=tg_id,
                            message_id=data["token_is_used"]
                        )
                    except Exception:
                        pass

                    try:
                        await self.bot.delete_message(
                            chat_id=tg_id,
                            message_id=data["incorrect_token"]
                        )
                    except Exception:
                        pass

                    try:
                        await self.bot.delete_message(
                            chat_id=tg_id,
                            message_id=data["used_token_message"]
                        )
                    except Exception:
                        pass

                await self.bot.delete_message(
                    chat_id=tg_id,
                    message_id=mess_id
                )

                async with state.proxy() as data:
                    data["token"] = text

                bot_info = await bot.me

                # await AddBotStates.step_1.set()
                text = f"Выбранный бот: @{bot_info.username}\n\n" \
                       f"Теперь давайте настроим вашего бота\n" \
                       f"1. Создайте новый канал, выберите тип канала “приватный”\n" \
                       f"2. Добавьте созданного бота в канал\n" \
                       f"3. Назначьте созданного бота администратором\n\n" \
                       f"В этом канале будет храниться переписка с пользователями, где вы сможете посмотреть диалог с конкретным клиентом.\n\n" \
                       f"После выполнения этих действий нажмите на кнопку ниже"

                # await self.bot.delete_message(
                #     chat_id=tg_id,
                #     message_id=loading_message.message_id
                # )
                #
                # step_1_message = await self.bot.send_message(
                #     chat_id=tg_id,
                #     text=text,
                #     reply_markup=InlineKeyboardMarkup().add(
                #         InlineKeyboardButton(text="Далее >>>", callback_data="to-2-step")
                #     )
                # )
                #
                # async with state.proxy() as data:
                #     data["step_1"] = step_1_message.message_id
                #     # data["bot_added_message"] = bot_added_message.message_id

            else:
                token_is_used = await self.bot.send_message(
                    chat_id=tg_id,
                    text="Данный токен уже используется",
                    reply_markup=menu
                )

                async with state.proxy() as data:
                    data["used_token_message"] = message.message_id
                    data["token_is_used"] = token_is_used.message_id
                    # print(data)

                # await self.bot.delete_message(
                #     chat_id=tg_id,
                #     message_id=loading_message.message_id
                # )

        except Exception as e:
            print(e)



    else:
        incorrect_token = await self.bot.send_message(
            chat_id=tg_id,
            text="Некорректный токен",
            reply_markup=menu
        )

        async with state.proxy() as data:
            data["incorrect_token"] = incorrect_token.message_id
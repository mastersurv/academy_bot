from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton
from utils.db_api.database import DataBase

from aiogram.types import Message, ContentTypes
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import menu, admin_menu

from handlers.constructor_callback_handler import constructor_callback_handler

from states_handlers.states import SettingsStates, MenuStates
from states_handlers.get_promocode_handler import get_promocode_handler
from states_handlers.get_promo_usage_handler import get_promo_usage_handler

from commands_handlers.set_group_handler import set_group_handler

from course_creation_handlers.edit_course_name import edit_course_name
from course_creation_handlers.edit_course_description import edit_course_description
from course_creation_handlers.edit_course_image import edit_course_image
from course_creation_handlers.edit_final_message import edit_final_message

from module_creation_handlers.edit_module_name import edit_module_name
from module_creation_handlers.edit_module_description import edit_module_description
from module_creation_handlers.edit_module_image import edit_module_image

from lesson_creation_handlers.edit_lesson_name import edit_lesson_name
from lesson_creation_handlers.edit_lesson_description import edit_lesson_description
from lesson_creation_handlers.edit_lesson_material import edit_lesson_material
from lesson_creation_handlers.test_question_handler import test_question_handler
from lesson_creation_handlers.test_keyboard_handler import test_keyboard_handler

from config import channel_id, group_id, easycourses_channel


class MyBot:
	def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
		self.bot = bot
		self.dp = dp
		self.db = db

	async def start_handler(self, message: Message, state: FSMContext):
		chat = message.chat.id
		tg_id = message.from_user.id
		username = message.from_user.username
		full_name = message.from_user.full_name
		if not username:
			username = full_name

		users = await self.db.get_users_ids()
		keyboard = menu
		keyboard = admin_menu  # TODO убрать
		# Если юзер подписчик канала - у него кнопки админа
		# is_member = await self.bot.get_chat_member(easycourses_channel, tg_id)

		# creators_ids = await self.db.get_creators_ids()
		# if tg_id in creators_ids:
		#     keyboard = admin_menu
		# if is_member.status == "member" or is_member.status == "creator" or is_member.status == "administrator":
		# 	keyboard = admin_menu

		await self.bot.send_message(
			chat_id=chat,
			text="Добро пожаловать в нашего бота!\n\n<b>Меню</b>",
			parse_mode="html",
			reply_markup=keyboard
		)

		if tg_id not in users:
			# Вызов метода добавления пользователя
			await self.db.add_user(tg_id, full_name)
			try:
				await self.dp.bot.send_message(
					chat_id=channel_id, text=f"Чат с пользователем @{username}",
				)

				reply_message = await self.dp.bot.send_message(
					chat_id=group_id,
					text="Новый чат",
				)
				await self.db.add_user_post(tg_id=tg_id, post_id=reply_message.message_id + 1)

			except Exception as e:
				print(e)

	async def text_handler(self, message: Message, state: FSMContext):
		print(message)
		tg_id = message.from_user.id
		m_id = message.message_id
		chat_type = message.chat.type
		if chat_type == "supergroup":
			try:
				if message.sender_chat is None or message.sender_chat.type != "channel":
					await self.dp.bot.copy_message(
						from_chat_id=message.chat.id,
						message_id=message.message_id,
						chat_id=await self.db.get_message_or_user(
							id=True,
							message_id=message.reply_to_message.message_id,
						)
					)
			except Exception as e:
				print(e)

		elif chat_type == "private":
			try:
				message_to_chat = await self.dp.bot.copy_message(
					chat_id=group_id,
					from_chat_id=tg_id,
					message_id=m_id,
					reply_to_message_id=await self.db.get_post_id(tg_id=tg_id)
				)
				await self.db.add_user_message(tg_id=tg_id, message_id=message_to_chat.message_id)

			except Exception as e:
				print(e)

	def register_handlers(self):
		self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")
		self.dp.register_message_handler(callback=set_group_handler, commands=["set_group"], state="*")
		self.dp.register_callback_query_handler(callback=constructor_callback_handler, state="*")

		self.dp.register_message_handler(callback=get_promocode_handler, content_types=["text"],
		                                 state=MenuStates.promocode)
		self.dp.register_message_handler(callback=get_promo_usage_handler, content_types=["text"],
										 state=MenuStates.n_promo)

		self.dp.register_message_handler(callback=edit_course_name, state=SettingsStates.course_name,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=edit_course_description, state=SettingsStates.course_description,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=edit_course_image, state=SettingsStates.course_image,
		                                 content_types=["photo"])
		self.dp.register_message_handler(callback=edit_final_message, state=SettingsStates.final_message,
		                                 content_types=ContentTypes.ANY)

		self.dp.register_message_handler(callback=edit_module_name, state=SettingsStates.module_name,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=edit_module_description, state=SettingsStates.module_description,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=edit_module_image, state=SettingsStates.module_image,
		                                 content_types=["photo"])

		self.dp.register_message_handler(callback=edit_lesson_name, state=SettingsStates.lesson_name,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=edit_lesson_description, state=SettingsStates.lesson_description,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=edit_lesson_material, state=SettingsStates.lesson_material,
		                                 content_types=ContentTypes.ANY)
		self.dp.register_message_handler(callback=test_question_handler, state=SettingsStates.test_question,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=test_keyboard_handler, state=SettingsStates.test_keyboard,
		                                 content_types=["text"])
		self.dp.register_message_handler(callback=self.text_handler, state="*", content_types=ContentTypes.ANY)

	def run(self):
		self.register_handlers()
		executor.start_polling(dispatcher=self.dp, skip_updates=True)

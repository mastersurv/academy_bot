from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext

from utils.functions.get_bot_and_db import get_bot_and_db

from utils.functions.generate_courses_markup import generate_courses_keyboard
from utils.functions.generate_modules_markup import generate_modules_keyboard
from utils.functions.generate_lessons_markup import generate_lessons_keyboard
from utils.functions.generate_created_courses_markup import generate_created_courses_keyboard
from utils.functions.generate_course_settings_markup import generate_courses_settings_keyboard
from utils.functions.generate_modules_settings_markup import generate_modules_settings_keyboard
from utils.functions.generate_lessons_settings_markup import generate_lessons_settings_keyboard
from utils.functions.generate_multi_markup import generate_multi_keyboard

from utils.functions.send_lesson import send_lesson

from states_handlers.states import SettingsStates, MenuStates
from blanks.bot_markup import (
	menu,
	to_menu,
	admin_menu,
	course_creation,
	to_course_creation,
	bot_settings_mp,
	modules_settings_mp,
	lessons_settings_mp,
	back_to_modules,
	back_to_lessons,
	back_to_settings
)


async def constructor_callback_handler(call: CallbackQuery, state: FSMContext):
	bot, db = get_bot_and_db()
	chat = call.message.chat.id
	tg_id = call.from_user.id
	callback = call.data
	m_id = call.message.message_id
	print(callback)
	# local_menu = menu
	local_menu = admin_menu  # TODO убрать

	if callback == "menu":
		creators_ids = await db.get_creators_ids()
		if tg_id in creators_ids:
			local_menu = admin_menu
		try:
			await bot.edit_message_text(
				chat_id=chat,
				message_id=m_id,
				text="<b>Меню</b>",
				parse_mode="html",
				reply_markup=local_menu
			)
		except Exception as e:
			print(e)

	elif callback == "library":
		courses_ids = await db.get_courses_ids(tg_id=tg_id)
		if len(courses_ids) == 0:
			try:
				await bot.edit_message_text(
					chat_id=chat,
					text="К сожалению у вас нет доступа ни к одному курсу",
					message_id=m_id,
					reply_markup=to_menu
				)
			except:
				pass

		else:
			keyboard = await generate_courses_keyboard(courses_ids_list=courses_ids)
			# await bot.edit_message_text(
			# 	chat_id=chat,
			# 	text="<b>Список ваших курсов:</b>",
			# 	parse_mode="html",
			# 	message_id=m_id,
			# 	reply_markup=keyboard
			# )
			await bot.delete_message(
				chat_id=chat,
				message_id=m_id
			)

			await bot.send_message(
				chat_id=chat,
				text="<b>Список ваших курсов:</b>",
				parse_mode="html",
				reply_markup=keyboard
			)


	elif callback == "get_course":
		await MenuStates.promocode.set()
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text="Чтобы получить доступ к курсам, у вас должен быть промокод, отправьте его нам и по кнопке 'Мои курсы' у вас появятся курсы",
				message_id=m_id,
				reply_markup=to_menu
			)
		except:
			pass

	elif callback == "buy_subscription":
		# TODO - генератор клавиатуры с ценами и ниже отслеживать subscription_{price}
		pass

	elif callback == "ask_question":
		await MenuStates.ask_question.set()
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text="Мы видим ваши сообщения в наш чат, задавайте вопросы в любое время и мы вам ответим",
				message_id=m_id,
				reply_markup=to_menu
			)
		except:
			pass

	elif callback == "courses_analytics":
		analytics_keyboard = await generate_created_courses_keyboard(tg_id=tg_id, analytics=True)
		text = "Выберите курс, аналитику по которому хотите посмотреть:"
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				reply_markup=analytics_keyboard.add(
					InlineKeyboardButton(
						text="В меню",
						callback_data="menu"
					)
				)
			)
		except:
			pass

	elif callback.startswith("course_analytic"):
		course_id = int(callback.split("_")[2])
		filename = "Как стать менеджером по продажам_аналитика.xlsx"
		with open(filename, "rb") as excel_file:
			await bot.send_document(
				chat_id=chat,
				document=excel_file.read(),
				caption='Аналитика по курсу'
			)

	elif callback == "creation_courses":
		course_number = await db.get_number_of_created_courses(tg_id=tg_id)
		subscription_data = await db.get_subscription_data()
		user_status = await db.get_subscription_status(tg_id=tg_id)
		# TODO: Реализация с количеством курсов, которые может создать пользователь
		# text = f"Число курсов, которое вы можете создать: {subscription_data[user_status] - course_number}"
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text="Создайте новый курс или отредактируйте созданные:",
				message_id=m_id,
				reply_markup=course_creation
			)
		except:
			pass

	elif callback == "created_courses":
		created_courses_keyboard = await generate_created_courses_keyboard(tg_id=tg_id)
		text = "Список созданных вами курсов"
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				reply_markup=created_courses_keyboard.add(
					InlineKeyboardButton(
						text="К созданию курсов",
						callback_data="creation_courses"
					)
				)
			)
		except:
			pass

	elif callback == "create_course":
		course_number = await db.get_number_of_created_courses(tg_id=tg_id)
		subscription_data = await db.get_subscription_data()
		user_status = await db.get_subscription_status(tg_id=tg_id)
		user_status = 'active'  # TODO: Реализация работы с проверкой подписки (статуса пользователя)
		# if subscription_data[user_status] - course_number > 0:
		if user_status:
			new_course_id = await db.generate_unique_course_id()
			async with state.proxy() as data:
				data["course_id"] = new_course_id
				data["mode"] = "creation"
			text = "Введите название курса:"
			await SettingsStates.course_name.set()

		else:
			text = "Количество курсов, которое вы можете создать достигло лимита"

		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				reply_markup=to_course_creation
			)
		except:
			pass

	elif callback[:15] == "course_settings":
		course_id = int(callback.split("_")[2])
		keyboard = await generate_courses_settings_keyboard(course_id=course_id)
		course_name = await db.get_course_name(course_id=course_id)
		text = f"Настройка вашего курса:\n<b>{course_name}</b>"

		try:
			await bot.delete_message(chat_id=chat, message_id=m_id)
			await bot.send_message(
				chat_id=chat, text=text,
				parse_mode="html",
				reply_markup=keyboard
			)
			# await bot.edit_message_text(
			# 	chat_id=chat,
			# 	text=text,
			# 	parse_mode='html',
			# 	message_id=m_id,
			# 	reply_markup=keyboard
			# )
		except:
			pass

	elif callback[:17] == "check_demo_course":
		course_id = int(callback.split("_")[3])
		course_name, course_description, course_image = await db.get_course_info(course_id=course_id)

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		text = f"<b>{course_name}</b>\n\n{course_description}"

		await bot.send_photo(
			chat_id=chat,
			photo=course_image,
			caption=text,
			reply_markup=InlineKeyboardMarkup().add(
				InlineKeyboardButton(
					text="Назад",
					callback_data=f"course_settings_{course_id}"
				)
			)
		)

	elif callback[:11] == "edit_course":
		mode = callback.split("_")[2]
		course_id = int(callback.split("_")[3])

		async with state.proxy() as data:
			data["course_id"] = course_id

		try:
			await bot.edit_message_reply_markup(
				chat_id=chat,
				message_id=m_id,
				reply_markup=back_to_settings
			)
		except:
			pass

		text = "Текст"
		if mode == "name":
			course_name = await db.get_course_name(course_id=course_id)
			text = f"Введите новое название курса.\nНынешнее название: <br>{course_name}</br>"
			await SettingsStates.course_name.set()
		elif mode == "description":
			course_description = await db.get_course_description(course_id=course_id)
			text = f"Введите новое описание курса.\nНынешнее описание: <pre>{course_description}</pre>"
			await SettingsStates.course_description.set()
		elif mode == "image":
			text = f"Отправьте в бота новую аватарку курса."
			await SettingsStates.course_image.set()
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				parse_mode="html"
			)
		except:
			pass

	elif callback.startswith("edit_final_message_"):
		course_id = int(callback.split("_")[3])

		async with state.proxy() as data:
			data["course_id"] = course_id

		text = "Отправьте финальное сообщение, это сообщение пользователи будут видеть, когда продут весь последний урок курса.\n" \
			   "Доступные форматы:\n" \
			   "1) Текст (поддерживается форматирование)\n" \
			   "2) Фото\n" \
			   "3) Фото с текстом\n" \
			   "4) Голосовое сообщение\n" \
			   "5) Видео\n" \
			   "6) Видеосообщение\n" \
			   "7) PDF-файлы\n"

		await SettingsStates.final_message.set()
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				parse_mode="html",
				reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(
						text="К настройке курса",
						callback_data=f"course_settings_{course_id}"
					)
				)
			)
		except:
			print(f"проблемы с колбэк: {callback}")

	elif callback[:10] == "add_module":
		course_id = int(callback.split("_")[2])
		new_module_id = await db.get_modules_numbers(course_id=course_id) + 1

		async with state.proxy() as data:
			data["course_id"] = course_id
			data["module_id"] = new_module_id
			data["mode"] = "creation"

		text = "Введите название модуля:"
		await SettingsStates.module_name.set()

		try:
			await bot.edit_message_text(
				text=text,
				chat_id=chat,
				message_id=m_id,
				reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(
						text="К настройке курса",
						callback_data=f"course_settings_{course_id}"
					)
				)
			)
		except Exception as e:
			print(e)

	elif callback[:15] == "created_modules":
		course_id = int(callback.split("_")[2])
		course_name = await db.get_course_name(course_id=course_id)
		created_modules_keyboard = await generate_modules_keyboard(course_id=course_id)
		text = f"Курс <b>{course_name}</b>\nСписок модулей:"
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				parse_mode="html",
				message_id=m_id,
				reply_markup=created_modules_keyboard
			)
		except Exception as e:
			print(e)

	elif callback[:15] == "module_settings":
		course_id = int(callback.split("_")[2])
		module_id = int(callback.split("_")[3])

		keyboard = await generate_modules_settings_keyboard(course_id=course_id, module_id=module_id)
		module_name = await db.get_module_name(course_id=course_id, module_id=module_id)
		text = f"Настройка вашего модуля:\n<b>{module_name}</b>"

		try:
			if call.message.photo:
				await bot.delete_message(
					chat_id=chat,
					message_id=m_id
				)

				await bot.send_message(
					chat_id=chat,
					text=text,
					parse_mode='html',
					reply_markup=keyboard
				)
			else:
				await bot.edit_message_text(
					chat_id=chat,
					text=text,
					parse_mode='html',
					message_id=m_id,
					reply_markup=keyboard
				)
		except Exception as e:
			print(e)

	elif callback[:11] == "edit_module":
		mode = callback.split("_")[2]
		course_id = int(callback.split("_")[3])
		module_id = int(callback.split("_")[4])

		async with state.proxy() as data:
			data["course_id"] = course_id
			data["module_id"] = module_id

		try:
			await bot.edit_message_reply_markup(
				chat_id=chat,
				message_id=m_id,
				reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(
						text="К настройке модуля",
						callback_data=f"module_settings_{course_id}_{module_id}"
					)
				)
			)
		except Exception as e:
			print(e)

		text = "Текст"
		if mode == "name":
			module_name = await db.get_module_name(course_id=course_id)
			text = f"Введите новое название модуля.\nНынешнее название: <br>{module_name}</br>"
			await SettingsStates.module_name.set()
		elif mode == "description":
			module_description = await db.get_module_description(course_id=course_id)
			text = f"Введите новое описание модуля.\nНынешнее описание: <pre>{module_description}</pre>"
			await SettingsStates.module_description.set()
		elif mode == "image":
			text = f"Отправьте в бота новую аватарку модуля."
			await SettingsStates.module_image.set()
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				parse_mode="html"
			)
		except:
			pass

	elif callback[:17] == "check_demo_module":
		course_id = int(callback.split("_")[3])
		module_id = int(callback.split("_")[4])
		module_name, module_description, module_image = await db.get_module_info(course_id=course_id,
		                                                                         module_id=module_id)

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		text = f"<b>{module_name}</b>\n\n{module_description}"
		print('here')

		await bot.send_photo(
			chat_id=chat,
			photo=module_image,
			caption=text,
			parse_mode='html',
			reply_markup=InlineKeyboardMarkup().add(
				InlineKeyboardButton(
					text="Назад",
					callback_data=f"module_settings_{course_id}_{module_id}"
				)
			)
		)

	elif callback[:15] == "created_lessons":
		course_id = int(callback.split("_")[2])
		module_id = int(callback.split("_")[3])

		module_name = await db.get_module_name(course_id=course_id, module_id=module_id)
		created_lessons_keyboard = await generate_lessons_keyboard(course_id=course_id, module_id=module_id)
		text = f"Модуль <b>{module_name}</b>\nСписок уроков:"
		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				parse_mode="html",
				message_id=m_id,
				reply_markup=created_lessons_keyboard.add(
					InlineKeyboardButton(
						text="К настройке модуля",
						callback_data=f"module_settings_{course_id}_{module_id}"
					)
				)
			)
		except:
			pass

	elif callback[:15] == "lesson_settings":
		course_id = int(callback.split("_")[2])
		module_id = int(callback.split("_")[3])
		lesson_id = int(callback.split("_")[4])

		keyboard = await generate_lessons_settings_keyboard(course_id=course_id, module_id=module_id,
		                                                    lesson_id=lesson_id)
		lesson_name = await db.get_lesson_info(course_id=course_id, module_id=module_id, lesson_id=lesson_id)
		lesson_name = lesson_name[0]
		text = f"Настройка вашего урока:\n<b>{lesson_name}</b>"

		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				parse_mode='html',
				message_id=m_id,
				reply_markup=keyboard
			)
		except:
			pass

	elif callback[:10] == "add_lesson":
		course_id = int(callback.split("_")[2])
		module_id = int(callback.split("_")[3])
		new_lesson_id = await db.get_lessons_numbers(course_id=course_id, module_id=module_id) + 1

		async with state.proxy() as data:
			data["course_id"] = course_id
			data["module_id"] = module_id
			data["lesson_id"] = new_lesson_id
			data["mode"] = "creation"

		text = "Введите название урока:"
		await SettingsStates.lesson_name.set()

		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(
						text="К настройке модуля",
						callback_data=f"module_settings_{course_id}_{module_id}"
					)
				)
			)
		except Exception as e:
			print(e)

	elif callback[:20] == "edit_lesson_material":
		course_id = int(callback.split("_")[3])
		module_id = int(callback.split("_")[4])
		lesson_id = int(callback.split("_")[5])

		async with state.proxy() as data:
			data["course_id"] = course_id
			data["module_id"] = module_id
			data["lesson_id"] = lesson_id

		try:
			await bot.edit_message_reply_markup(
				chat_id=chat,
				message_id=m_id,
				reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(
						text="К настройке урока",
						callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
					)
				)
			)
		except:
			pass

		text = "Отправьте материал к уроку, доступные форматы:\n" \
		       "1) Текст (поддерживается форматирование)\n" \
		       "2) Фото\n" \
		       "3) Фото с текстом\n" \
		       "4) Голосовое сообщение\n" \
		       "5) Видео\n" \
		       "6) Видеосообщение\n" \
		       "7) PDF-файлы\n"

		await SettingsStates.lesson_material.set()

		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				parse_mode="html"
			)
		except:
			pass

	elif callback[:11] == "edit_lesson":
		mode = callback.split("_")[2]
		course_id = int(callback.split("_")[3])
		module_id = int(callback.split("_")[4])
		lesson_id = int(callback.split("_")[5])

		async with state.proxy() as data:
			data["course_id"] = course_id
			data["module_id"] = module_id
			data["lesson_id"] = lesson_id

		try:
			await bot.edit_message_reply_markup(
				chat_id=chat,
				message_id=m_id,
				reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(
						text="К настройке урока",
						callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
					)
				)
			)
		except:
			pass

		text = "Текст"
		if mode == "name":
			lesson_name = await db.get_lesson_name(course_id=course_id, module_id=module_id)
			text = f"Введите новое название урока.\nНынешнее название: <br>{lesson_name}</br>"
			await SettingsStates.lesson_name.set()
		elif mode == "description":
			lesson_description = await db.get_lesson_description(course_id=course_id, module_id=module_id)
			text = f"Введите новое описание урока.\nНынешнее описание: <pre>{lesson_description}</pre>"
			await SettingsStates.lesson_description.set()

		try:
			await bot.edit_message_text(
				chat_id=chat,
				text=text,
				message_id=m_id,
				parse_mode="html"
			)
		except:
			pass

	elif callback[:12] == "add_homework":
		course_id = int(callback.split("_")[2])
		module_id = int(callback.split("_")[3])
		lesson_id = int(callback.split("_")[4])

		async with state.proxy() as data:
			data["course_id"] = course_id
			data["module_id"] = module_id
			data["lesson_id"] = lesson_id

		await bot.edit_message_text(
			chat_id=chat,
			message_id=m_id,
			text="Введите вопрос для тестового задания",
			reply_markup=InlineKeyboardMarkup().add(
				InlineKeyboardButton(
					text="К настройкам курса",
					callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
				)
			)
		)

		await SettingsStates.test_question.set()

	elif callback[:13] == "choose_answer":
		right_answer = int(callback.split("_")[2])
		course_id = int(callback.split("_")[3])
		module_id = int(callback.split("_")[4])
		lesson_id = int(callback.split("_")[5])

		await bot.edit_message_reply_markup(
			chat_id=chat,
			message_id=m_id,
			reply_markup=InlineKeyboardMarkup()
		)

		async with state.proxy() as data:
			test_question = data["test_question"]
			test_keyboard = data["test_keyboard"]

		new_test_id = await db.get_test_numbers(course_id=course_id, module_id=module_id, lesson_id=lesson_id) + 1
		await db.add_test_question(course_id=course_id, module_id=module_id, lesson_id=lesson_id, test_id=new_test_id,
		                           test_question=test_question, right_answer=right_answer)
		for num, answer in enumerate(test_keyboard):
			await db.add_test_answer(course_id=course_id, module_id=module_id, lesson_id=lesson_id, test_id=new_test_id,
			                         answer_num=num, answer=answer)

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		await bot.send_message(
			chat_id=chat,
			text=f"На вопрос: <b>{test_question}</b>\n"
			     f"Выбран ответ: <b>{test_keyboard[right_answer]}</b>",
			parse_mode="html",
			reply_markup=InlineKeyboardMarkup().add(
				InlineKeyboardButton(
					text="Тест добавлен (к настройкам)",
					callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
				)
			).add(
				InlineKeyboardButton(
					text="Изменить ответ",
					callback_data=f"edit_test_answer_{new_test_id}_{course_id}_{module_id}_{lesson_id}"
				)
			).add(
				InlineKeyboardButton(
					text="Добавить новый тест",
					callback_data=f"add_homework_{course_id}_{module_id}_{lesson_id}"
				)
			)
		)

	elif callback[:16] == "edit_test_answer":
		test_id = int(callback.split("_")[3])
		course_id = int(callback.split("_")[4])
		module_id = int(callback.split("_")[5])
		lesson_id = int(callback.split("_")[6])

		await db.delete_test_question(course_id=course_id, module_id=module_id, lesson_id=lesson_id, test_id=test_id)
		await db.delete_test_answer(course_id=course_id, module_id=module_id, lesson_id=lesson_id, test_id=test_id)

		async with state.proxy() as data:
			test_question = data["test_question"]
			test_keyboard = data["test_keyboard"]

		keyboard = InlineKeyboardMarkup()
		for num, elem in enumerate(test_keyboard):
			keyboard.add(
				InlineKeyboardButton(
					text=elem,
					callback_data=f"choose_answer_{num}_{course_id}_{module_id}_{lesson_id}"
				)
			)

		await bot.edit_message_text(
			chat_id=chat,
			message_id=m_id,
			text=f"Выберите ВЕРНЫЙ вариант ответа.\n<b>{test_question}</b>",
			parse_mode="html",
			reply_markup=keyboard
		)

	elif callback[:17] == "check_demo_lesson" or callback[:6] == "lesson":
		if callback[:6] == "lesson":
			course_id = int(callback.split("_")[1])
			module_id = int(callback.split("_")[2])
			lesson_id = int(callback.split("_")[3])
		elif callback[:17] == "check_demo_lesson":
			course_id = int(callback.split("_")[3])
			module_id = int(callback.split("_")[4])
			lesson_id = int(callback.split("_")[5])

		lesson_name, text, voice_id, photo_id, video_id, video_note_id, document_id = await db.get_lesson_info(
			course_id=course_id, module_id=module_id, lesson_id=lesson_id)
		if not text:
			text = ''

		keyboard = InlineKeyboardMarkup().add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
			)
		)

		if callback[:6] == "lesson":
			keyboard = await generate_multi_keyboard(course_id=course_id, module_id=module_id, lesson_id=lesson_id,
			                                         test_id=None)  # TODO func
			# keyboard = InlineKeyboardMarkup().add(
			#     InlineKeyboardButton(
			#         text="Назад",
			#         callback_data=f"module_{course_id}_{module_id}"
			#     )
			# )

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		await send_lesson(
			bot=bot,
			chat_id=chat,
			lesson_name=lesson_name,
			text=text,
			audio=voice_id,
			photo=photo_id,
			video=video_id,
			video_note=video_note_id,
			document=document_id,
			markup=keyboard
		)

	elif callback[:6] in ["course", "module"]:
		course_id = int(callback.split("_")[1])

		if callback[:6] == "course":
			name, description, image_id = await db.get_course_info(course_id=course_id)
			keyboard = await generate_modules_keyboard(course_id=course_id, passing=True)

		else:
			module_id = int(callback.split("_")[2])
			name, description, image_id = await db.get_module_info(course_id=course_id, module_id=module_id)
			keyboard = await generate_lessons_keyboard(course_id=course_id, module_id=module_id, passing=True)

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		await bot.send_photo(
			chat_id=chat,
			caption=f"<b>{name}</b>\n\n{description}",
			parse_mode="html",
			photo=image_id,
			reply_markup=keyboard
		)

	elif callback.startswith("final_message_"):
		course_id = int(callback.split("_")[2])
		text, voice_id, photo_id, video_id, video_note_id, document_id = await db.get_final_message(course_id=course_id)
		course_name = await db.get_course_name(course_id=course_id)

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		await send_lesson(
			bot=bot,
			lesson_name=course_name,
			chat_id=chat,
			text=text,
			audio=voice_id,
			photo=photo_id,
			video=video_id,
			video_note=video_note_id,
			document=document_id,
			markup=InlineKeyboardMarkup().add(
				InlineKeyboardButton(
					text="В начало курса",
					callback_data=f"course_{course_id}"
				)
			)
		)

	elif callback[:4] == "test":
		course_id = int(callback.split("_")[1])
		module_id = int(callback.split("_")[2])
		lesson_id = int(callback.split("_")[3])
		test_id = int(callback.split("_")[4])
		test_question, right_answer = await db.get_test_question(course_id=course_id, module_id=module_id,
		                                                         lesson_id=lesson_id, test_id=test_id)
		keyboard = await generate_multi_keyboard(course_id=course_id, module_id=module_id,
		                                         lesson_id=lesson_id, test_id=test_id)

		await bot.delete_message(
			chat_id=chat,
			message_id=m_id
		)

		await bot.send_message(
			chat_id=chat,
			text=test_question,
			reply_markup=keyboard
		)

	elif callback[:6] == "answer":
		course_id = int(callback.split("_")[1])
		module_id = int(callback.split("_")[2])
		lesson_id = int(callback.split("_")[3])
		test_id = int(callback.split("_")[4])
		answer_id = int(callback.split("_")[5])

		test_question, right_answer = await db.get_test_question(course_id=course_id, module_id=module_id,
		                                                         lesson_id=lesson_id, test_id=test_id)
		# test_answer_id, test_answer_text = await db.get_test_answers(course_id=course_id, module_id=module_id,
		#                                                             lesson_id=lesson_id, test_id=test_id)

		l_text = list()
		l_data = list()
		cd = call.message.reply_markup.inline_keyboard
		is_right = False

		for elem in cd:
			text = elem[0]

		for l_el in cd:
			for el in l_el:

				text = el["text"]
				callback_data = el["callback_data"]
				# print(data, "DATA")
				print(callback_data, callback)

				if len(callback_data.split("_")) == 6 and callback_data.split("_")[5] == right_answer and callback_data == callback:
					text = "✅ " + text
					is_right = True

				elif callback_data == callback:
					text = "❌ " + text

				l_data.append(callback_data)
				l_text.append(text)

		# print(l_text, l_data)
		next_text, next_button = await generate_multi_keyboard(course_id=course_id, module_id=module_id,
		                                                       lesson_id=lesson_id, test_id=test_id,
		                                                       answer=True)

		i_mp = InlineKeyboardMarkup()
		count = 0
		for text, ca in zip(l_text, l_data):
			if is_right and len(l_data) - count - 1 == 0:
				i_mp.add(
					InlineKeyboardButton(
						text=next_text,
						callback_data=next_button
					)
				)
			else:
				i_mp.add(
					InlineKeyboardButton(
						text=text,
						callback_data=ca
					)
				)

			count += 1

		await bot.edit_message_reply_markup(
			chat_id=chat,
			message_id=m_id,
			reply_markup=i_mp
		)

			# if text == test_question:
			# 	for l_el in cd:
			# 		for el in l_el:
			#
			# 			text = el["text"]
			# 			callback_data = el["callback_data"]
			# 			# print(data, "DATA")
			# 			if callback_data.split("_")[5] == right_answer:
			# 				text = "✓ " + text
			# 				is_right = True
			#
			# 			else:
			# 				text = "крестик " + text
			#
			# 			l_data.append(callback_data)
			# 			l_text.append(text)
			#
			# 	# print(l_text, l_data)
			# 	next_text, next_button = await generate_multi_keyboard(course_id=course_id, module_id=module_id,
			# 	                                                       lesson_id=lesson_id, test_id=test_id,
			# 	                                                       answer=True)
			#
			# 	i_mp = InlineKeyboardMarkup()
			# 	count = 0
			# 	for text, ca in zip(l_text, l_data):
			# 		if is_right and len(l_data) - count - 1 == 0:
			# 			i_mp.add(
			# 				InlineKeyboardButton(
			# 					text=next_text,
			# 					callback_data=next_button
			# 				)
			# 			)
			# 		else:
			# 			i_mp.add(
			# 				InlineKeyboardButton(
			# 					text=text,
			# 					callback_data=ca
			# 				)
			# 			)
			#
			# 		count += 1
			#
			# 	await bot.edit_message_reply_markup(
			# 		chat_id=chat,
			# 		message_id=m_id,
			# 		reply_markup=i_mp
			# 	)

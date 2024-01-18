from aiogram import Bot
import os


async def send_lesson(bot: Bot, chat_id, text, audio, photo, video, video_note, document, markup=None, lesson_name=None):
    funnel_message = 0
    if photo is not None:
        try:
            funnel_message = await bot.send_photo(
                chat_id=chat_id,
                caption=f"<b>{lesson_name}</b>\n\n" + text,
                photo=photo,
                parse_mode="html",
                reply_markup=markup,

            )

        except Exception as e:
            print(e)

    elif video_note is not None:
        try:
            funnel_message = await bot.send_video_note(
                chat_id=chat_id,
                video_note=video_note,
                reply_markup=markup
            )
        except Exception as e:
            print(e)

    elif video is not None:
        try:
            funnel_message = await bot.send_video(
                chat_id=chat_id,
                video=video,
                reply_markup=markup,
                caption=f"<b>{lesson_name}</b>\n\n" + text,
                parse_mode="html"
            )
        except Exception as e:
            print(e)

    elif audio is not None:
        try:
            funnel_message = await bot.send_voice(
                chat_id=chat_id,
                voice=audio,
                caption=f"<b>{lesson_name}</b>\n\n" + text,
                reply_markup=markup
            )
        except Exception as e:
            print(e)

    elif document:
            funnel_message = await bot.send_document(
                chat_id=chat_id,
                document=document,
                caption=f"<b>{lesson_name}</b>\n\n" + text,
                parse_mode="html",
                reply_markup=markup,
            )

    elif text is not None:
        text = f"<b>{lesson_name}</b>\n\n" + text if lesson_name else text
        try:
            funnel_message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="html",
                reply_markup=markup,
                disable_web_page_preview=True
            )
        except Exception as e:
            print(e)

    return funnel_message
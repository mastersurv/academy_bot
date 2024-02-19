
async def files_ids(message, bot):
    photo_id = None
    text = None
    voice_id = None
    video_id = None
    video_note_id = None
    document_id = None

    if message.photo:
        photo_id = message.photo[-1].file_id
        if message.caption:
            text = message.html_text

    elif message.voice:
        voice_id = message.voice.file_id

    elif message.video:
        video_id = message.video.file_id

        if message.caption:
            text = message.html_text

    elif message.video_note:
        video_note_id = message.video_note[-1].file_id

    elif message.document:
        file = await bot.get_file(message.document.file_id)
        file_path = file.file_path

        if file_path.endswith(".pdf"):
            document_id = message.document.file_id

            if message.caption:
                text = message.html_text

    elif message.text:
        text = message.html_text

    return text, voice_id, photo_id, video_id, video_note_id, document_id
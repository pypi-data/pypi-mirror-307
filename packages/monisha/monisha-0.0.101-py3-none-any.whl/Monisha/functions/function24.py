
class Pyrogram:

    async def get01(update):
        return (update.video or
                update.audio or
                update.voice or
                update.document or update.video_note)

import logging
import os
from PIL import Image

from pyrogram import filters, Client

from sample_config import Config
from translation import Translation
import database.database as sql

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

app = Client("RenameBot", bot_token=Config.TG_BOT_TOKEN, api_id=Config.APP_ID, api_hash=Config.API_HASH)

@app.on_message(filters.photo)
async def save_photo(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id, revoke=True)
        return

    download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/"
    if update.media_group_id is not None:
        download_location += str(update.media_group_id) + "/"
        
    # Create download directory if not exist
    if not os.path.isdir(download_location):
        os.makedirs(download_location)
        
    # Download media
    await sql.df_thumb(update.from_user.id, update.message_id)
    await bot.download_media(message=update, file_name=download_location)

@app.on_message(filters.command(["delthumb"]))
async def delete_thumbnail(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id, revoke=True)
        return

    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    
    try:
        await sql.del_thumb(update.from_user.id)
    except:
        pass
    
    try:
        os.remove(thumb_image_path)
    except:
        pass

    await bot.send_message(chat_id=update.chat.id, text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL, reply_to_message_id=update.message_id)

@app.on_message(filters.command(["showthumb"]))
async def show_thumb(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id, revoke=True)
        return

    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    
    if not os.path.exists(thumb_image_path):
        mes = await sql.thumb(update.from_user.id)
        if mes is not None:
            m = await bot.get_messages(update.chat.id, mes.msg_id)
            await m.download(file_name=thumb_image_path)
        else:
            thumb_image_path = None    
    
    if thumb_image_path is not None:
        try:
            await bot.send_photo(chat_id=update.chat.id, photo=thumb_image_path, reply_to_message_id=update.message_id)
        except:
            pass
    else:
        await bot.send_message(chat_id=update.chat.id, text=Translation.NO_THUMB_FOUND, reply_to_message_id=update.message_id)

app.run()

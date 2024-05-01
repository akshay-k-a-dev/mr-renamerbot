
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters 
from pyrogram import Client as Mai_bOTs

#from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram

from pyrogram.errors import UserNotParticipant, UserBannedInChannel 
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from database.database import *
from database.db import *

@startanimeff.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry, You're Banned")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Due To The Huge Traffic Only Channel Members Can Use This Bot Means You Need To Join The Below Mentioned Channel Before Using Me! **",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📝Rename', callback_data = "rnme"),
                    InlineKeyboardButton('📂File To Video', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('🎞️Custom Thumbnail', callback_data = "cthumb"),
                    InlineKeyboardButton('📑Custom Caption', callback_data = "ccaption")
                ],
                [
                    InlineKeyboardButton('💬About', callback_data = "about")
                ]
            ]
        )
    )       

@Mai_bOTs.on_message(pyrogram.filters.command(["start"]))
async def start_me(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry,You've Been Flooding Me So My Owner Removed You From Using Me If You Think It's An Error Contact : @Faris_TG")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Due To The Huge Traffic Only Channel Members Can Use This Bot Means You Need To Join The Below Mentioned Channel Before Using Me! **",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("Help", callback_data = "ghelp")
                ],
                [
                    InlineKeyboardButton('Support Channel', url='https://t.me/startanimeff'),
                    InlineKeyboardButton('Feedback', url='https://techmobilitymalayalam.simdif.com')
                ],
                [
                    InlineKeyboardButton('Other Bots', url='https://github.com/Akshay-code-space/mr-renamerbot'),
                    InlineKeyboardButton('Source', url='https://github.com/Akshay-code-space/mr-renamerbot')
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
            return 

@Mai_bOTs.on_callback_query()
async def cb_handler(client: Mai_bOTs , query: CallbackQuery):
    data = query.data
    if data == "rnme":
        await query.message.edit_text(
            text=Translation.RENAME_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "f2v":
        await query.message.edit_text(
            text=Translation.C2V_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "ccaption":
        await query.message.edit_text(
            text=Translation.CCAPTION_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Show Current Caption', callback_data = "shw_caption"),
                    InlineKeyboardButton("Delete Caption", callback_data = "d_caption")
                ],
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton('🔒 Close', callback_data = "close")
                ]
            ]
        )
     )
    elif data == "cthumb":
        await query.message.edit_text(
            text=Translation.THUMBNAIL_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "closeme":
        await query.message.delete()
        try:
            await query.message.reply_text(
                text = "<b>Process Cancelled</b>"
     )
        except:
            pass 
    elif data == "ghelp":
        await query.message.edit_text(
            text=Translation.HELP_USER,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📝Rename', callback_data = "rnme"),
                    InlineKeyboardButton('📂File To Video', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('🎞️Custom Thumbnail', callback_data = "cthumb"),
                    InlineKeyboardButton('📑Custom Caption', callback_data = "ccaption")
                ],
                [
                    InlineKeyboardButton('💬About', callback_data = "about")
                ]
            ]
        )
    )       

    elif data =="shw_caption":
             try:
                caption = await get_caption(query.from_user.id)
                c_text = caption.caption
             except:
                c_text = "Sorry but you haven't added any caption yet please set your caption through /scaption command" 
             await query.message.edit(
                  text=f"<b>Your Custom Caption:</b> \n\n{c_text} ",
                  parse_mode="html", 
                  disable_web_page_preview=True, 
                  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ccaption"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "about":
        await query.message.edit_text(
            text=Translation.ABOUT_ME,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "d_caption":
        try:
           await del_caption(query.from_user.id)   
        except:
            pass
        await query.message.edit_text(
            text="<b>caption deleted successfully</b>",
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ccaption"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

import threading
import asyncio
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import os

from sqlalchemy.orm import sessionmaker, scoped_session

import os

import threading
import asyncio

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, UniqueConstraint, func

from sample_config import Config

def start() -> scoped_session:
    engine = create_engine(Config.DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class custom_caption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)
    
    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

custom_caption.__table__.create(checkfirst=True)

async def update_cap(id, caption):
    with INSERTION_LOCK:
        cap = SESSION.query(custom_caption).get(id)
        if not cap:
            cap = custom_caption(id, caption)
            SESSION.add(cap)
            SESSION.flush()
        else:
            SESSION.delete(cap)
            cap = custom_caption(id, caption)
            SESSION.add(cap)
        SESSION.commit()

async def del_caption(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_caption).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def get_caption(id):
    try:
        caption = SESSION.query(custom_caption).get(id)
        return caption
    finally:
        SESSION.close()

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import pyrogram

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation
from pyrogram import filters
from pyrogram import Client as MaI_BoTs

import database.database as sql
from PIL import Image
from database.database import *

@MaI_BoTs.on_message(filters.photo)
async def save_photo(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return

    if update.media_group_id is not None:
        # album is sent
        download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/" + str(update.media_group_id) + "/"
        # create download directory, if not exist
        if not os.path.isdir(download_location):
            os.makedirs(download_location)
        await sql.df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
    else:
        # received single photo
        download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
        await sql.df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.SAVED_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.message_id
        )

@MaI_BoTs.on_message(filters.command(["delthumb"]))
async def delete_thumbnail(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
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

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )

@MaI_BoTs.on_message(filters.command(["showthumb"]))
async def show_thumb(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return

    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    if not os.path.exists(thumb_image_path):
        mes = await thumb(update.from_user.id)
        if mes != None:
            m = await bot.get_messages(update.chat.id, mes.msg_id)
            await m.download(file_name=thumb_image_path)
            thumb_image_path = thumb_image_path
        else:
            thumb_image_path = None    
    
    if thumb_image_path is not None:
        try:
            await bot.send_photo(
                chat_id=update.chat.id,
                photo=thumb_image_path,
                reply_to_message_id=update.message_id
            )
        except:
            pass
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.NO_THUMB_FOUND,
            reply_to_message_id=update.message_id
        )

# Run the bot
Mai_bOTs.run()


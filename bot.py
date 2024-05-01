import logging
import os

import pyrogram

from config import Config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
        
    plugins = dict(root="plugins")
    
    app = pyrogram.Client(
        "RenameBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    
    # Add your Telegram ID to the authorized users
    Config.AUTH_USERS.add(861055237)
    Config.AUTH_USERS.add(5491384523)
    
    app.run()

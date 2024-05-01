from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from sample_config import Config

import threading

# Define global variables for database setup
engine = create_engine(Config.DB_URI, client_encoding="utf8")
BASE = declarative_base()
SESSION = scoped_session(sessionmaker(bind=engine, autoflush=False))

# Define table structure for custom_caption
class CustomCaption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)
    
    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

# Create the table if not exists
BASE.metadata.create_all(engine)

# Lock for thread safety
INSERTION_LOCK = threading.RLock()

# Function to start the session
def start_session() -> scoped_session:
    return SESSION()

# Function to add or update custom caption data
async def update_custom_caption(id, caption):
    session = start_session()
    with INSERTION_LOCK:
        try:
            custom_caption = session.query(CustomCaption).get(id)
            if not custom_caption:
                custom_caption = CustomCaption(id=id, caption=caption)
                session.add(custom_caption)
            else:
                custom_caption.caption = caption
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Function to delete custom caption data
async def delete_custom_caption(id):
    session = start_session()
    with INSERTION_LOCK:
        try:
            custom_caption = session.query(CustomCaption).get(id)
            if custom_caption:
                session.delete(custom_caption)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Function to get custom caption data
async def get_custom_caption(id):
    session = start_session()
    try:
        custom_caption = session.query(CustomCaption).get(id)
        return custom_caption
    except Exception as e:
        raise e
    finally:
        session.close()

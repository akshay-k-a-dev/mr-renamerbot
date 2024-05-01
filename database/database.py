from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from sample_config import Config

import threading

# Define global variables for database setup
engine = create_engine(Config.DB_URI, client_encoding="utf8")
BASE = declarative_base()
SESSION = scoped_session(sessionmaker(bind=engine, autoflush=False))

# Define table structure for Thumbnail
class Thumbnail(BASE):
    __tablename__ = "thumbnail"
    id = Column(Integer, primary_key=True)
    msg_id = Column(Integer)
    
    def __init__(self, id, msg_id):
        self.id = id
        self.msg_id = msg_id

# Create the table if not exists
BASE.metadata.create_all(engine)

# Lock for thread safety
INSERTION_LOCK = threading.RLock()

# Function to start the session
def start_session() -> scoped_session:
    return SESSION()

# Function to add or delete thumbnail data
async def manage_thumbnail(id, msg_id, delete=False):
    session = start_session()
    with INSERTION_LOCK:
        try:
            if delete:
                session.query(Thumbnail).filter(Thumbnail.id == id).delete()
            else:
                thumbnail = Thumbnail(id=id, msg_id=msg_id)
                session.merge(thumbnail)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Function to get thumbnail data
async def get_thumbnail(id):
    session = start_session()
    try:
        thumbnail = session.query(Thumbnail).filter(Thumbnail.id == id).first()
        return thumbnail
    except Exception as e:
        raise e
    finally:
        session.close()

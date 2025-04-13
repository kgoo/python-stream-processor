from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Aggregate, Base
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def store_aggregate(compound_key, count):
    session = Session()
    try:
        value, window = compound_key
        window_start_ts = datetime.fromtimestamp(window[0], tz=timezone.utc)

        logger.info(f"store_aggregate: value={value}, count={count}, window_start={window_start_ts}")

        agg = session.get(Aggregate, {"value": value, "window_start": window_start_ts})
        if agg:
            logger.info("Updating existing aggregate")
            agg.count = count
        else:
            logger.info("Creating new aggregate")
            agg = Aggregate(value=value, window_start=window_start_ts, count=count)
            session.add(agg)

        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"DB error: {e}")
    finally:
        session.close()



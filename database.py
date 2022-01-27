import logging
import os
from typing import Optional

import sqlalchemy
from slack_sdk.oauth.installation_store import InstallationStore
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore
from sqlalchemy.engine import Engine
from config import SLACK_CLIENT_ID, SQL_URI

engine: Optional[Engine] = None
installation_store: Optional[InstallationStore] = None

logger = logging.getLogger(__name__)
database_url = SQL_URI

logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
engine = sqlalchemy.create_engine(database_url)
installation_store = SQLAlchemyInstallationStore(
    client_id=SLACK_CLIENT_ID,
    engine=engine,
    logger=logger,
)
oauth_state_store = SQLAlchemyOAuthStateStore(
    expiration_seconds=120,
    engine=engine,
    logger=logger,
)

def run_db_migration():
	try:
			engine.execute("select count(*) from slack_bots")
	except Exception as _:
			installation_store.metadata.create_all(engine)
			oauth_state_store.metadata.create_all(engine)

run_db_migration()



import os
import logging
from typing import List
from sqlmodel import create_engine, Session, SQLModel

from models import *
from configs.constant_config import constants

POSTGRES_URL = os.getenv(
    "POSTGRES_URL") or "postgresql://postgres:password@localhost/testth"


# global ENGINE_SETTED
# ENGINE_SETTED = False
# global SESSION_SETTED
# SESSION_SETTED = False


class InitializePostgres:
    def __init__(
            self,
            url: str = POSTGRES_URL,
            _engine=None,
            _session=None
    ):
        self.url = url
        self._engine = _engine
        self._session = _session

    def set_engine(self):
        # global ENGINE_SETTED
        # if ENGINE_SETTED == False:
        engine = create_engine(self.url, echo=True)
        self._engine = engine
            # ENGINE_SETTED = True

    @property
    def engine(self):
        self.set_engine()
        return self._engine

    def set_session(self):
        # global SESSION_SETTED
        # if SESSION_SETTED == False:
        self._session = Session(self.engine)
            # SESSION_SETTED = True

    @property
    def session(self):
        self.set_session()
        return self._session

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def insert_networks(self):
        for network_type in NetworkType:
            network = Network(id=network_type.value, name=network_type.name)
            try:
                with self.session as session:
                    session.add(network)
                    session.commit()
            except Exception as e:
                logging.exception(e)

    def insert_chains(self):
        for chain_id in Chain.supported_chains():
            chain = constants.chains[chain_id]
            chain = Chain(**chain)
            try:
                with self.session as session:
                    session.add(chain)
                    session.commit()
            except Exception as e:
                logging.exception(e)

    def insert_addresses(self, address: str, network_id: int):
        address = Address(address=address, networkId=network_id)
        try:
            with self.session as session:
                session.add(address)
                session.commit()
        except Exception as e:
            logging.exception(e)

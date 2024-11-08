"""
SqlAlchemy ORM for tracking OCR

See ao-google-books/README.md for requirements explanation

Initially, this creates a standalone DB which imports work_ids from the DRS database
We would like to get to declaring the data classes using Reflection, but we need to try
the actual import and creation from logs first.

Pattern is from  https://medium.com/dataexplorations/sqlalchemy-orm-a-more-pythonic-
way-of-interacting-with-your-database-935b57fd2d4d


"""

import configparser
import logging
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from BdrcDbLib.SqlAlchemy_get_or_create import get_or_create

from BdrcDbLib.DBConfig import DBConfig
from BdrcDbLib.DbOrm.models.drs import *



Base = declarative_base()

# VVVVVVVVV     is development - Toggle off in production VVVVVVVVV
is_dev: bool = False


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


class OcrTrackException(Exception):
    pass


class DrsDbContextBase:
    """
    Maintains and defines DRS Tables. Full ORM implementation
    """

    # Static class member so other apps can use it. (as DrsContextBase.bdrc_db_conf
    bdrc_db_conf: str = None
    _default_bdrc_db_conf: str = f"{'qa' if is_dev else 'prod'}:~/.config/bdrc/db_apps.config"

    def __init__(self, context_str: str = None):
        """
        use a given context, if you have one
        """
        self.drs_engine = None
        self.drs_session = None
        self.bdrc_db_conf = context_str if context_str is not None else DrsDbContextBase._default_bdrc_db_conf

    @property
    def session(self) -> Session:
        return self.get_session()


    def get_session(self):
        """
        Singleton session manager
        :return: session object - note this is not defined until it is created
        """
        global Session
        if self.drs_engine is None:
            self.drs_engine = self.connect_db()
            # Wacko, but SQL Alchemy is all about class generation
            Session = sessionmaker(bind=self.drs_engine, expire_on_commit=False)
            self.drs_session = Session(future=True)
        return self.drs_session

    def get_engine(self):
        if self.drs_engine is None:
            self.get_session()
        return self.drs_engine


    def close_session(self,commit: bool = False):
        if self.drs_session is not None:
            try:
                if commit:
                    self.drs_session.flush()
                    self.drs_session.commit()
                else:
                    self.drs_session.rollback()
            finally:
                self.drs_session.close()
        if self.drs_engine is not None:
            self.drs_engine.dispose()
        self.drs_engine = None
        self.drs_session = None


    def connect_db(self, create_db=False):
        """
        See the build_db() procedure to configure how to run a CREATE method with
        the correct privileges. After creating from the model, the ordinary drsclient user
        should be able to CRUD.
        Once, you have to run this as a user with CREATE privileges, if you are updating any of the models
        here. Ordinary run is as the client
        :param create_db: True only if modifying and updating DDL from model (see build_db)
        """

        # We need to reach through the BdrcDbLib config into the underlying [mysql] config
        # parser
        _cnf: [str] = self.bdrc_db_conf.split(':')
        drs_cnf: DBConfig = DBConfig(_cnf[0], _cnf[1])

        engine_cnf = configparser.ConfigParser()
        engine_cnf.read(os.path.expanduser(drs_cnf.db_cnf))

        drs_conn_str = "mysql+mysqldb://%s:%s@%s:%d/%s" % (
            engine_cnf.get(drs_cnf.db_host, "user"),
            engine_cnf.get(drs_cnf.db_host, "password"),
            engine_cnf.get(drs_cnf.db_host, "host"),
            engine_cnf.getint(drs_cnf.db_host, "port", fallback=3306),
            engine_cnf.get(drs_cnf.db_host, "database"))

        engine = create_engine(drs_conn_str, echo=False, future=True)

        if create_db:
            bobby_tables: [] = [
                Works().__table__,
                Volumes().__table__,
                GbContent().__table__,
                GbDownload().__table__,
                GbMetadata().__table__,
                GbState().__table__,
                GbDistribution().__table__,
                GbUnpack().__table__,
                GbReadyTrack().__table__
            ]

            Base.metadata.create_all(engine, checkfirst=True, tables=bobby_tables)

        return engine

    def __enter__(self):
        self.get_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        commit: bool = exc_type is None
        self.close_session(commit)

    def get_some_works(self) -> [Works]:
        """
        Test shell. See https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
        for starters
        :return:
        """
        return self.session.query(Works).filter(Works.WorkName == 'W1FPL2251').all()

    def get_work_by_name(self, work_name: str) -> Works:
        """
        Get work by Name
        :param work_name: work to fetch
        :return: MySQL ORM object
        """
        return self.session \
            .query(Works) \
            .filter(Works.WorkName == work_name) \
            .first()

    def get_or_create_work(self, work_name: str) -> Works:
        """
        Get or create an object managed in this session
        :param work_name: create or get by work name only
        as you need
        :return: object which matches the input filter, or a new object with the
        **kwargs attributes
        """
        #
        # required to construct, might not be given in input
        defaults = {"HOLLIS": '0'}
        o, newly_made = get_or_create(self.session, Works, defaults, WorkName=work_name)
        if (newly_made):
            logging.debug(f"Newly made {o}")
        return o

    def get_or_create_volume(self, work_name: str, volume_name: str):
        vol_work: Works = self.get_or_create_work(work_name)
        o, newly_made = get_or_create(self.session, Volumes, label=volume_name, work=vol_work)
        if (newly_made):
            logging.debug(f"Newly made {o}")
        return o

    def get_downloads(self):
        """
        Gets all the downloads
        """
        from sqlalchemy import select
        # query from a class
        statement = select(GbDownload).order_by(GbDownload.download_time)

        # list of first element of each row (i.e. User objects)
        return self.session.execute(statement).fetchall()

    def remove_volumes(self, labels: [str]):
        """
        Removes a list of volumes identified by their label
        !! Don't use in productionDon't generally use this!
        :param labels: list of volumes to remove
        :return:
        """
        vols2 = self.session.query(Volumes).filter(Volumes.label.in_(labels)).all()
        for vv in vols2:
            self.session.delete(vv)
        self.session.commit()

    def remove_works(self, work_names: [str]):
        """
        Removes a list of works identified by their WorkName.
        !! Don't use in production
        :param work_names:
        :return:
        """
        works = self.session.query(Works).filter(Works.WorkName.in_(work_names)).all()
        for w in works:
            self.session.delete(w)
        self.session.commit()


def build_db(config: str):
    logging.basicConfig(datefmt='[ %Z: %Y-%m-%d %X ]', format='%(asctime)s%(levelname)s:%(message)s',
                        level=logging.INFO)
    try:
        logging.info("creating database objects....")

        # vvvvvvvvv  FOR DEVELOPMENT - creating objects vvvvvvvvvvv
        # bdrc_db_config = 'qa'
        #  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # vvvvvvvvv  FOR PRODUCTION - creating objects vvvvvvvvvvv
        section = 'prodsa'
        #  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        with DrsDbContextBase(config) as ctx:
            ctx.connect_db(create_db=True)
        logging.info("created.")

    except:
        ei = sys.exc_info()
        logging.error(f"Could not create database objects {ei[1]}")


if __name__ == '__main__':
    build_db('qa:~/.config/bdrc/db_apps.config')

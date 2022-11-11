# external imports
from sqlalchemy import create_engine, Column, MetaData, Table, and_
# from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session
# from sqlalchemy.sql import func

# internal imports
from datetime import datetime, timedelta

# local imports
from tools import utils

Base = declarative_base()
Metadata = MetaData()

Notes = Table(
    "notes",
    Metadata,
    Column("_id", Integer, primary_key=True),
    Column("uuid", Integer, nullable=False),
    Column("cost", Integer),
    Column("category", String(20)),
    Column("comment", String(100)),
    Column("timestamp", DateTime(timezone=True), default=datetime.now()),
)

class Note(Base):
    __table__ = Notes

# class Note(Base):
#     __tablename__ = "notes"
#     _id = Column(Integer, primary_key=True)
#     uuid = Column(Integer)
#     cost = Column(Integer)
#     category = Column(String)
#     timestamp = Column(DateTime(timezone=True), default=datetime.now())


class Database:
    def __init__(self, engine, dev):
        self.engine = create_engine(engine, echo=dev)
        Metadata.create_all(self.engine)
        
    def _open(self):
        try:
            self.session = Session(self.engine)

            # self.conn = self.engine.connect()
            return 0
        except Exception as err:
            return err

    def _close(self):
        self.session.close()
        # self.conn.close()

    def category_is_exist(self, uuid, category):
        err = self._open()
        if err:
            return False, err
        output = self.session.query(Note).\
            filter_by(
                uuid=uuid,
                category=category,  
            ).first()
        self._close()
        if output:
            return True, None
            
        return False, None

    def create_one(self, object):
        err = self._open()
        if err:
            return False, err
        self.session.add(object)
        self.session.commit()
        self._close()
        return True, None
    
    def get_notes(self, uuid, scope="last_month"):
        err = self._open()
        if err:
            return {}, err

        today = datetime.today()
        if scope == "last_month":
            start = today.replace(month=today.month-1, day=1)
            end = today.replace(day=1) - timedelta(days=1)
        elif scope == "current_month":
            start = today.replace(day=1)
            end = today.replace(month=today.month+1, day=1) - timedelta(days=1)

        output = self.session.query(Note.cost, Note.category).\
            filter(and_(Note.uuid == uuid, \
                Note.timestamp > start, 
                Note.timestamp < end))
        self._close()
        notes = utils.init_dict_from_list(output)
        for cost, category in output:
            notes[category.title()] += cost
        return notes, None

    # def get_last_week(self, uuid):
    #     notes = self.get_notes_by_days_ago(uuid, 7)
    #     return notes, None
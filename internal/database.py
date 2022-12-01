# external imports
from sqlalchemy import create_engine, Column, MetaData, Table, ForeignKey
from sqlalchemy import select, and_
# from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session, relationship
# from sqlalchemy.sql import func

# internal imports
from datetime import datetime, timedelta

# local imports
from tools import utils
import operator

Base = declarative_base()
Metadata = MetaData()

Users = Table(
    "users",
    Metadata,
    Column("_id", Integer, primary_key=True),
    Column("uuid", Integer, nullable=False, unique=True)
)

Notes = Table(
    "notes",
    Metadata,
    Column("_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users._id")),
    Column("cost", Integer),
    Column("category", String(50)),
    Column("comment", String(100)),
    Column("timestamp", DateTime(timezone=True), default=datetime.now()),
)

LimitC = Table(
    "limits",
    Metadata,
    Column("_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users._id")),
    Column("category", String(50)),
    Column("limit", Integer),
)


class Note(Base):
    __table__ = Notes
    
class Limits(Base):
    __table__ = LimitC

class User(Base):
    __table__ = Users
    limits = relationship("Limits")
    notes = relationship("Note")

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
        user_id = select(User._id).where(User.uuid == uuid)
        presql = select(Note.category).\
            where(and_(Note.user_id == user_id, Note.category == category))
        output = self.session.execute(presql).first()
        self._close()
        if output:
            return True, None
            
        return False, None

    def create_note(self, uuid, note):
        err = self._open()
        if err:
            return False, err
        user = self.session.query(User).filter_by(uuid=uuid).first()
        if not user:
            user = User(uuid=uuid)
            self.session.add(user)
        user.notes.append(note)

        self.session.commit()
        self._close()
        return True, None

    def get_categories(self, uuid):
        err = self._open()
        if err: return {}, err
        user_id = select(User._id).where(User.uuid == uuid)
        categories = self.session.query(Note.category).\
            filter(Note.user_id==user_id).distinct()
        self._close()
        return [x[0] for x in categories], None

    def trigger_by_limit(self, uuid, category):
        limit, err = self.get_limit_by_category(uuid, category)
        if not limit or err:
            return False, err
        err = self._open()
        if err: return False, err
        today = datetime.today()
        start = today.replace(day=1, hour=0, minute=0)
        if today.month == 12:
            end = today.replace(month=12, day=31)
        else:
            end = today.replace(month=today.month+1, day=1) - timedelta(days=1)
        user_id = select(User._id).where(User.uuid == uuid)
        summa = self.session.query(Note.cost).\
            filter(
                Note.user_id == user_id, 
                Note.category == category,
                Note.timestamp > start, 
                Note.timestamp < end,
                ).all()
        self._close()
        if sum([s[0] for s in summa]) > limit: return True, None
        return False, None

    def get_limit_by_category(self, uuid, category):
        err = self._open()
        if err:return None, err
        user_id = select(User._id).where(User.uuid == uuid)
        limit = self.session.query(Limits.limit).\
            filter(Limits.user_id==user_id, Limits.category==category).first()
        self._close()
        if limit is None:
            return limit, None
        return limit[0], None

    def get_limit_all(self, uuid):
        err = self._open()
        if err: return None, err
        user_id = select(User._id).where(User.uuid == uuid)
        limits = self.session.query(Limits.category, Limits.limit).\
            filter(Limits.user_id==user_id, Limits.limit > 0).all()
        self._close()
        if not limits:
            return None, None
        return limits, None

    def update_limit_by_category(self, uuid, category, new_limit):
        err = self._open()
        if err: return err
        limit, err = self.get_limit_by_category(uuid, category)
        user_id = select(User._id).where(User.uuid == uuid)
        if err: return err
        elif limit is None:
            user = self.session.query(User).filter_by(uuid=uuid).first()
            user.limits.append(Limits(category=category, limit=new_limit))
        elif limit != new_limit:
            l = self.session.query(Limits).\
                filter(Limits.user_id==user_id, Limits.category==category).first()
            l.limit = new_limit
        self.session.commit()
        self._close()
        return None

    def get_notes(self, uuid, scope="last_month"):
        """
        Get notes by scope datetime
        Scope - [last_month, current_month]
        """
        err = self._open()
        if err:
            return {}, err

        today = datetime.today()
        if scope == "last_month":
            start = today.replace(month=today.month-1, day=1, hour=0, minute=0)
            end = today.replace(day=1) - timedelta(days=1)
        elif scope == "current_month":
            start = today.replace(day=1, hour=0, minute=0)
            if today.month == 12:
                end = today.replace(month=12, day=31)
            else: 
                end = today.replace(month=today.month+1, day=1) - timedelta(days=1)
        user_id = select(User._id).where(User.uuid == uuid)
        presql = select(Note.cost, Note.category).\
            where(and_(Note.user_id==user_id,
                Note.timestamp > start, 
                Note.timestamp < end)).order_by(Note.cost.desc())
        output = self.session.execute(presql).all()
        self._close()
        notes = utils.init_dict_from_list(output)
        for cost, category in output:
            notes[category.title()] += cost
        return notes, None

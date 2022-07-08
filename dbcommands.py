from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, Session
from datetime import date


base = declarative_base()

engine = create_engine("sqlite:///users.db")


class User(base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    games_played = Column(Integer)
    games_won = Column(Integer)
    session_date = Column(Date)

# base.metadata.create_all(engine)

def create_user(**params):
    with Session(engine) as session:
        new_user = User(username=params['username'], games_played=params["games_played"],
                        games_won=params["games_won"], session_date=date.today())
        session.add_all([new_user])
        session.commit()

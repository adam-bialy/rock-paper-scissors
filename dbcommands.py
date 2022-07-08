from sqlalchemy import create_engine, select, desc, asc
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from datetime import date, datetime


base = declarative_base()

engine = create_engine("sqlite:///users.db")


class User(base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    games_played = Column(Integer)
    games_won = Column(Integer)
    session_date = Column(Date, nullable=False)


class Game(base):
    __tablename__ = "game"

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    won = Column(Boolean, nullable=False)
    credits_before = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


def create_user(**params):
    with Session(engine) as session:
        new_user = User(username=params['username'], games_played=params["games_played"],
                        games_won=params["games_won"], session_date=date.today())
        session.add_all([new_user])
        session.commit()
        return new_user.user_id


def write_game(user_id, won, creds):
    with Session(engine) as session:
        new_game = Game(user_id=user_id, won=won, credits_before=creds, timestamp=datetime.now())
        session.add_all([new_game])
        session.commit()


def update_user(**params):
    with Session(engine) as session:
        user = session.query(User).filter(User.user_id == params["user_id"])
        user.update({"games_played": params["games_played"], "games_won": params["games_won"]})
        session.commit()


def get_top():
    with engine.connect() as conn:
        command = select(User.username, User.games_played, User.games_won).\
            where(User.session_date == date.today()).\
            order_by(desc("games_won"), desc("games_played"), asc("username")).limit(5)
        return conn.execute(command).fetchall()


if __name__ == "__main__":
    base.metadata.create_all(engine)

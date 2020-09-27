from database.base import Base
from sqlalchemy import Column, String, Integer
from utility import coins


class Game(Base):
    __tablename__ = "game"

    game_id = Column(String, index=True, primary_key=True)
    row_num = Column(Integer,primary_key=True)
    column_num = Column(Integer,primary_key=True)
    cell_value = Column(Integer, default=0)


class NextCoin(Base):
    __tablename__ = "nextcoin"
    game_id = Column(String,index=True,primary_key=True)
    next_coin = Column(Integer,default=coins.Coins.yellow.value)


# class GameLogs(base):
#     __tablename__ = "gamelogs"
#
#     game_id = Column(String)
#     move_
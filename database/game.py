from sqlalchemy.orm import Session
from models.game import NextCoin, Game
from fastapi import HTTPException, status
from utility import coins


def check_if_game_id_exists(game_id: str, db: Session):
    return db.query(NextCoin).filter(NextCoin.game_id == game_id).first()


def get_next_coin_value_to_be_added(game_id, db: Session):
    return db.query(NextCoin).filter(NextCoin.game_id == game_id).first()


def get_game_matrix(game_id, db: Session):
    return db.query(Game).filter(Game.game_id == game_id)


def create_new_game(game_id, db: Session):
    new_game = NextCoin(game_id=game_id)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


def add_next_coin(game_id: str, column_number: int, row_number: int, coin_object:NextCoin, db: Session):
    try:
        new_coin_entry = Game(
            game_id=game_id,
            column_num=column_number,
            row_num=row_number,
            cell_value=coin_object.next_coin
        )
        db.add(new_coin_entry)
        db.commit()
        db.refresh(new_coin_entry)

        update_next_coin_for_game_id(coin_object, db)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="some error occurred")


def update_next_coin_for_game_id( coin_object, db ):
    if coin_object.next_coin == coins.Coins.yellow.value:
        setattr(coin_object, "next_coin", coins.Coins.red.value)
    else:
        setattr(coin_object, "next_coin", coins.Coins.yellow.value)

    db.commit()
    db.refresh(coin_object)

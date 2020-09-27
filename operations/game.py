import uuid
from database import game as game_db_operation
from sqlalchemy.orm import Session
from schemas import game
from models import game as game_model
import settings
from fastapi import HTTPException, status


def generate_game_id():
    return str(uuid.uuid1())[:6]


def update_game_board(game_id, column_number, db: Session):
    nextcoin: game.NextCoin = game_db_operation.get_next_coin_value_to_be_added(game_id, db)
    game_matrix = game_db_operation.get_game_matrix(game_id, db)
    local_game_matrix = [[0 for i in range(settings.COLUMN_SIZE)] for j in range(settings.ROW_SIZE)]
    obj: game_model
    for obj in game_matrix:
        local_game_matrix[obj.row_num][obj.column_num] = obj.cell_value

    desired_column = list(list(zip(*local_game_matrix))[column_number])
    try:
        next_row = desired_column.index(0)
        value_copied = nextcoin.next_coin
        game_db_operation.add_next_coin(game_id, column_number, next_row, nextcoin, db)

        local_game_matrix[next_row][column_number] = value_copied

        return local_game_matrix, next_row, column_number, value_copied

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID")



def check_for_winner(game_matrix, row_number, column_number):
    value_to_check = game_matrix[row_number][column_number]
    c = 1
    row_op = row_number - 1
    while row_op >= 0:
        if game_matrix[row_op][column_number] == value_to_check:
            c += 1
            if c == 4:
                return True
            row_op -= 1
        else:
            break
    c = 1
    row_op = row_number + 1
    while row_op < settings.ROW_SIZE:
        if game_matrix[row_op][column_number] == value_to_check:
            c += 1
            if c == 4:
                return True
            row_op += 1
        else:
            break
    col_op = column_number + 1
    c = 1
    while col_op < settings.COLUMN_SIZE:
        if game_matrix[row_number][col_op] == value_to_check:
            c += 1
            if c == 4:
                return True
            col_op += 1
        else:
            break
    col_op = column_number - 1
    c = 1
    while col_op >= 0:
        if game_matrix[row_number][col_op] == value_to_check:
            c += 1
            if c == 4:
                return True
            col_op -= 1
        else:
            break

    row_op = row_number-1
    col_op = column_number - 1
    c = 1
    while row_op >=0 and col_op >= 0:
        if game_matrix[row_op][col_op] == value_to_check:
            c += 1
            if c == 4:
                return True
            row_op -= 1
            col_op -= 1
        else:
            break

    row_op = row_number + 1
    col_op = column_number + 1
    c = 1
    while row_op < settings.ROW_SIZE and col_op < settings.COLUMN_SIZE:
        if game_matrix[row_op][col_op] == value_to_check:
            c += 1
            if c == 4:
                return True
            row_op += 1
            col_op += 1
        else:
            break

    row_op = row_number - 1
    col_op = column_number + 1
    c = 1
    while row_op >= 0 and col_op < settings.COLUMN_SIZE:
        if game_matrix[row_op][col_op] == value_to_check:
            c += 1
            if c == 4:
                return True
            row_op -= 1
            col_op += 1
        else:
            break

    row_op = row_number + 1
    col_op = column_number - 1
    c = 1
    while row_op < settings.ROW_SIZE and col_op >= 0:
        if game_matrix[row_op][col_op] == value_to_check:
            c += 1
            if c == 4:
                return True
            row_op += 1
            col_op -= 1
        else:
            break

    return False


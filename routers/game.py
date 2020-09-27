from fastapi import APIRouter, Response, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from operations import game as game_operations
from database import game as game_db_operations
from utility import db_dep

router = APIRouter()


@router.post("/start")
def start_game(response: Response, db: Session = Depends(db_dep.get_db)):
    game_id = game_operations.generate_game_id()
    new_game = game_db_operations.create_new_game(game_id, db)
    response.headers["game_id"] = new_game.game_id
    return "READY"


@router.post("/{column}")
def update_column(column: int, request: Request, db: Session = Depends(db_dep.get_db)):
    game_id = request.headers["game_id"]
    if not game_id:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game ID not provided")
    if not game_db_operations.check_if_game_id_exists(game_id, db):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game ID not found")
    try:
        game_matrix, row_number, column_number, coin = game_operations.update_game_board(game_id, column, db)
        if game_operations.check_for_winner(game_matrix, row_number, column_number):
            if coin == 1:
                return "Red Wins"
            else:
                return "Yellow Wins"
    except:
        return "INVALID"

    return "VALID"

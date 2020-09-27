from pydantic import BaseModel


class NextCoin(BaseModel):
    game_id: str
    next_coin: int

    class Config:
        orm_mode = True


class Game(BaseModel):
    game_id: str
    row_num: int
    column_num: int
    cell_value: int

    class Config:
        orm_mode = True

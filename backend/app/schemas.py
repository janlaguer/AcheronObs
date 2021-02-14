from typing import List, Optional

from pydantic import BaseModel


class Player(BaseModel):
    id: int
    real_name: str
    display_name: str
    country: Optional[str] = None
    portrait: Optional[str] = None
    agent: str = 'undefined'
    hp: int = 100
    ultimate_up: bool = False


class Team(BaseModel):
    id: int
    full_name: str
    short_name: str
    logo: Optional[str] = None
    players: List[Player]
    game_score: int = 0
    map_score: int = 0


class Match(BaseModel):
    id: int
    map: str = None
    spike_status: bool = None
    teams: List[Team]

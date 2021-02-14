import json

from fastapi import FastAPI
import cv2
from .hp_logic import get_healthpercent
from .schemas import Match
from .spike_logic import is_spike_planted
from .ultimate_logic import is_ultimate_up
from .score_logic import get_score


with open('ressource/config.json') as config_file:
    settings = json.load(config_file)

app = FastAPI()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

match = Match(id=1, spike_status=False,
              teams=[{'id': i,
                      'full_name': f'Team {i}',
                      'short_name': f'TM{i}',
                      'players': [{'id': i,
                                   'real_name': f'Player {i}',
                                   'display_name': f'Player {i}'} for i in range(0, 5)]
                      } for i in range(0, 2)]
              )


@app.post("/api/match/edit_match")
async def edit_match(new_match: Match):
    global match
    match = new_match
    return new_match


@app.get("/api/match/get_match/")
async def get_match():
    match.spike_status = await is_spike_planted(cap)
    match.teams[0].game_score = await get_score(settings['score_left_position'], cap)
    match.teams[1].game_score = await get_score(settings['score_right_position'], cap)
    for i in range(0, 5):
        match.teams[0].players[i].hp = await get_healthpercent(settings['team_1'][f'player_{i}_position'], cap)
        match.teams[0].players[i].ultimate_up = await is_ultimate_up(settings['team_1'][f'player_{i}_position'], cap)
    for i in range(0, 5):
        match.teams[1].players[i].ultimate_up = await is_ultimate_up(settings['team_2'][f'player_{i}_position'], cap)
        match.teams[1].players[i].hp = await get_healthpercent(settings['team_2'][f'player_{i}_position'], cap)
    return match


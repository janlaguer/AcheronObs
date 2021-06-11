import json
import requests
import cv2
import time
import hp_logic
import spike_logic
import ultimate_logic
import score_logic


with open('ressource/config.json') as config_file:
    settings = json.load(config_file)

cap = cv2.VideoCapture(settings['camera_index'], cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

match = {
    'id': 1,
    'map': 'ascent',
    'spike_status': False,
    'teams': [{
        'id': i,
        'full_name': f'Team {i}',
        'short_name': f'TM{i}',
        'logo': 'logo',
        'players': [{
            'id': x,
            'real_name': f'Player {x}',
            'display_name': f'Player {x}',
            'country': 'Philippines',
            'portrait': 'filename',
            'agent': 'agent',
            'hp': 100,
            'ultimate_up': False,
        } for x in range(0,5)],
        'game_score': 0,
        'map_score': 0,
    } for i in range(0,2)]
}


def get_match():
    match['spike_status'] = spike_logic.is_spike_planted(cap)
    match['teams'][0]['game_score'] = score_logic.get_score(settings['score_left_position'], cap)
    match['teams'][1]['game_score'] = score_logic.get_score(settings['score_right_position'], cap)
    for i in range(0, 5):
        match['teams'][0]['players'][i]['hp'] = hp_logic.get_healthpercent(settings['team_1'][f'player_{i}_position'], cap)
        match['teams'][0]['players'][i]['ultimate_up'] = ultimate_logic.is_ultimate_up(settings['team_1'][f'player_{i}_position'], cap)
    for i in range(0, 5):
        match['teams'][1]['players'][i]['ultimate_up'] = ultimate_logic.is_ultimate_up(settings['team_2'][f'player_{i}_position'], cap)
        match['teams'][1]['players'][i]['hp'] = hp_logic.get_healthpercent(settings['team_2'][f'player_{i}_position'], cap)
    return match

while True:
    # posts every 1 seconds to deta api server
    payload = get_match()
    r = requests.post('https://8lr09u.deta.dev/api/match/edit_match/', json=payload)
    print(f'POST result: {r}')
    time.sleep(1)
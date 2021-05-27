# NOT MAINTAINED, FORK IF YOU WANT.


# Acheron
[![volkswagen status](https://auchenberg.github.io/volkswagen/volkswargen_ci.svg?v=1)](https://github.com/auchenberg/volkswagen)

Acheron provides an API that can be used to create an observer HUD for the game Valorant.

It's a work in progress, if you wanna help feel free to contact me ! (frontend dev especially)

## Running Acheron
- pip install -r requirements.txt
- Install the latest build of Tesseract (https://github.com/UB-Mannheim/tesseract/wiki)
- Install OBS (https://github.com/obsproject/obs-studio)
- Install OBS Virtual camera (https://obsproject.com/forum/resources/obs-virtualcam.949/)
- Make a new scene on OBS with a game capture and activate the virtual camera output.
- You must position yourself so that the top of the game HUD is a black portion of the map (go under the map) like in the following screenshot :

![Alt text](screenshots/positionning.png?raw=true "Positionning")

- You can also use one of the provided screenshots (see the screenshots folder) for testing.
- python main.py to start the API server
- Navigate to http://localhost:8000/docs/ for the documentation
- get_match is the main endpoint and returns a json formatted response that you can use on your frontend.
- You can use edit_match to edit the match (team names, player names...)

## Troubleshooting
- If it doesn't work check that OBS' virtual camera is camera_index 0 (it may not be if you have additionals webcams installed). If that's the case you need to edit backend/ressource/config.json ("camera_index").
- Other issues ? Contact me with details.

## Todo
- Add scoreboard cv (weapons, money...) ?

## Contact & License
- julian.libercedeville@gmail.com
- https://twitter.com/aAa_pechz

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>

Images are property of their respective owners.

Riot Games does not endorse or sponsor this project.

## Exemple json response (get_match)
```json
{
  "id": 0,
  "map": "string",
  "spike_status": true,
  "teams": [
    {
      "id": 0,
      "full_name": "string",
      "short_name": "string",
      "logo": "string",
      "players": [
        {
          "id": 0,
          "real_name": "string",
          "display_name": "string",
          "country": "string",
          "portrait": "string",
          "agent": "undefined",
          "hp": 100,
          "ultimate_up": false
        }
      ],
      "game_score": 0,
      "map_score": 0
    }
  ]
}
```


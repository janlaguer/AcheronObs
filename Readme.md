# Acheron
[![volkswagen status](https://auchenberg.github.io/volkswagen/volkswargen_ci.svg?v=1)](https://github.com/auchenberg/volkswagen)

This product is aimed at improving the viewing experience in Valorant by providing data that can be used to create a custom HUD that can be integrated to a live broadcast.

It is using computer vision to gather information on the game (hp of the players, round time, and scores).

Only a bandaid until Riot releases a better way to do this (local telemetry data, game API, spectator API...)

## Example
![Screenshot](2.JPG "Screenshot")

## Running Acheron
- python AcheronObs.py
- java -jar acheron_overlay.jar

You need to create a 'config.json' file, see AcheronObs.py to see what's needed in this file.
Don't forget to install the requirements.

You can access the HUD at localhost:PORT/overlay and the Dashboard at localhost:PORT/dashboard.

It requires OBS Virtual Cam. Launch OBS and start the camera before AcheronObs.

## Support the project
If you use it in a professional setting it's always appreciated, I also can provide support if you plan on doing so.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XYYFJQKB5JGHJ&source=url)



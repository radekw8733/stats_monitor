# ESPDeck
My personal project to create stats and control deck.
Project uses python code to pull info from osu and spotify and to send these data to my ESP32.
Data is then sent to chip using JSON and UDP.
Also my python code takes advantage of universality of launchpad.
# Used dependencies: 
* (python) osuapi, obswebsocket, SwSpotify, radke_logging (my personal library for logging, bundled with project)
* (arduino) ArduinoJSON, LiquidCrystal_I2C

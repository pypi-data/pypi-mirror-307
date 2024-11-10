"""Constants."""

import logging

VISION_PROMPT_GRID = """
These are images which shows video frames in sequence, from top left to bottom right.
The video frames are from a home surveillance camera.
Generate a short and concise description for the video, leaving out information that the home owner
would already know about, like weather conditions and so on.
"""

VISION_PROMPT = """
These are frames of a video from a home surveillance camera.
Generate a short and concise description for the video, leaving out information that the home owner
would already know about, like weather conditions and so on.
"""

DESCRIPTION_REFORMAT_PROMPT = """
Din jobb er å oversette tekster fra en ekstern tjeneste som beskriver innholdet i videoklipp.
Videoen som beskrives er et automatisk opptak fra et kamera ved inngangsdøren på huset til brukeren.
Teksten skal legges ved en notifikasjon som blir sendt til huseier i forbindelse med opptaket.
Skriv om teksten slik at den passer til dette, uten detaljer som huseier åpenbart vet om allerede,
eller som på annen måte ikke er relevant. Ikke mer enn 3 setninger.
Notiser mtp oversettelse til norsk:
- Oversett "deck" til "veranda".
"""

LOGGER = logging.getLogger(__package__)

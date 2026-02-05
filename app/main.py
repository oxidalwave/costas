#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epaper
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import statsapi

DISPLAY_CODE = "epd7in5_V2"

REFRESH_RATE_IN_SECONDS = 5

START_DATE = '07/01/2024'
END_DATE = '07/31/2024'
TEAM_CODE = 'min'

def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        epd = epaper.epaper(DISPLAY_CODE).EPD()
        
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        teams = statsapi.lookup_team(TEAM_CODE)
        logging.info(f"Searching for team {TEAM_CODE}")
        logging.info(f"Found teams: {teams}")
        if (len(teams) != 1):
            logging.error(f"No team found for code {TEAM_CODE}")
            return
        team = teams[0]
        logging.info(f"Displaying schedule for {team['name']}")

        """ nextGameId = statsapi.next_game(team['id'])
        if (not nextGameId):
            logging.error(f"No upcoming games found for team {team['name']}")
            return
        
        nextGame = statsapi.boxscore_data(nextGameId)
        if (not nextGame):
            logging.error(f"Could not retrieve boxscore for game ID {nextGameId}")
            return """

        previousSchedule = None
        while (True):
            epd.init_fast()
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            schedule = statsapi.schedule(start_date=START_DATE,end_date=END_DATE,team=team['id'])
            if (previousSchedule != schedule):
                logging.debug(f"Schedule updated: {json.dumps(schedule, indent=2)}")
                for i, game in enumerate(schedule):
                    logging.debug(f"Drawing text: {game['summary']}")
                    draw.text((10, 10 + i * 30), game['summary'], font = font24, fill = 0)
                logging.debug("Updating display")
                epd.display_Partial(epd.getbuffer(Himage),0, 0, epd.width, epd.height)
                previousSchedule = schedule
            else:
                logging.debug("Schedule unchanged, skipping update")
            time.sleep(REFRESH_RATE_IN_SECONDS)
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epaper.epaper(DISPLAY_CODE).epdconfig.module_exit(cleanup=True)
        exit()

if __name__ == "__main__":
    main()

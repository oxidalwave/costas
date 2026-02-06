#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from config import Config
import logging
import epaper
import time
from PIL import Image,ImageDraw,ImageFont
import statsapi

def getTeamByCode(teamCode: str):
    teams = statsapi.lookup_team(teamCode)
    logging.info(f"Searching for team {teamCode}")
    logging.info(f"Found teams: {teams}")
    if (len(teams) != 1):
        logging.error(f"No team found for code {teamCode}")
        return None
    return teams[0]

def drawBoxscore(epd, boxscore):
    return

def main():
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Loading configuration")
    config = Config()
    configJson = json.dumps({
        'displayCode': config.getDisplayCode(),
        'refreshRateInSeconds': config.getRefreshRateInSeconds(),
        'startDate': config.getStartDate(),
        'endDate': config.getEndDate(),
        'teamCode': config.getTeamCode()
    }, indent=2)
    logging.debug(f"Configuration loaded: {configJson}")

    try:
        epd = epaper.epaper(config.getDisplayCode()).EPD()
        
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        teamCode = config.getTeamCode()
        team = getTeamByCode(teamCode)
        if (not team):
            logging.error(f"Could not find team for code {teamCode}, exiting")
            return
        logging.info(f"Displaying schedule for {team['name']}")

        previousData = None
        while (True):
            if (teamCode != config.getTeamCode()):
                logging.info("Team code changed, updating team info")
                teamCode = config.getTeamCode()
                team = getTeamByCode(teamCode)
                if (not team):
                    logging.error(f"Could not find team for code {teamCode}, exiting")
                    return
                logging.info(f"Displaying schedule for {team['name']}")

            data = {
                'scorebug': {
                    'away': {
                        'teamCode': 'NYY',
                        'score': '0'
                    },
                    'home': {
                        'teamCode': team['teamCode'],
                        'score': '3'
                    }
                }
            }

            epd.init_fast()

            if (previousData != data):
                logging.debug(f"Data updated: {json.dumps(data, indent=2)}")

                Himage = Image.new('1', (epd.width / 2, epd.height / 8), 255) # 255: clear the frame
                draw = ImageDraw.Draw(Himage)
                
                draw.text((2, 2), data['away']['teamCode'], font=font, fill = 0)
                draw.text((2, 28), data['home']['teamCode'], font=font, fill = 0)
                draw.text((202, 2), data['away']['score'], font=font, fill = 0)
                draw.text((202, 28), data['home']['score'], font=font, fill = 0)

                logging.debug("Updating display")
                epd.display(epd.getbuffer(Himage))

                previousData = data
            else:
                logging.debug("Schedule unchanged, skipping update")

            time.sleep(config.getRefreshRateInSeconds())
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epaper.epaper(config.getDisplayCode()).epdconfig.module_exit(cleanup=True)
        exit()

if __name__ == "__main__":
    main()

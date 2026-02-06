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
import time
from PIL import ImageFont
import statsapi

from ui import EpdDevice, render
from ui.examples import scorebug

FONT_SIZE = 24

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
        device = EpdDevice(config.getDisplayCode())

        logging.info("init and Clear")
        device.init()
        device.clear()

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
                        'teamCode': 'nyy',
                        'score': '0'
                    },
                    'home': {
                        'teamCode': team['teamCode'],
                        'score': '3'
                    }
                },
                'atBat': {
                    'batter': {
                        'name': 'Batter Name',
                        'wpa+': '110',
                    },
                    'pitcher': {
                        'name': 'Pitcher Name',
                        'era': '3.75',
                        'pitches': '42'
                    }
                }
            }

            device.init_fast()

            if (previousData != data):
                logging.debug(f"Data updated: {json.dumps(data, indent=2)}")

                image = render(
                    scorebug,
                    {"font": font, "data": data},
                    width=device.width,
                    height=device.height,
                )

                logging.debug("Updating display")
                device.display(image)

                previousData = data
            else:
                logging.debug("Schedule unchanged, skipping update")

            time.sleep(config.getRefreshRateInSeconds())
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        device.cleanup()
        exit()

if __name__ == "__main__":
    main()

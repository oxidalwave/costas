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

def getFontSize(displayCode: str):
    if (displayCode == 'epd7in5_V2'):
        return 24
    return 18

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

        fontSize = getFontSize(config.getDisplayCode())
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), fontSize)

        teamCode = config.getTeamCode()
        team = getTeamByCode(teamCode)
        if (not team):
            logging.error(f"Could not find team for code {teamCode}, exiting")
            return
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
            if (teamCode != config.getTeamCode()):
                logging.info("Team code changed, updating team info")
                teamCode = config.getTeamCode()
                team = getTeamByCode(teamCode)
                if (not team):
                    logging.error(f"Could not find team for code {teamCode}, exiting")
                    return
                logging.info(f"Displaying schedule for {team['name']}")
            epd.init_fast()
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            schedule = statsapi.schedule(start_date=config.getStartDate(), end_date=config.getEndDate(), team=team['id'])
            if (previousSchedule != schedule):
                logging.debug(f"Schedule updated: {json.dumps(schedule, indent=2)}")
                for i, game in enumerate(schedule):
                    logging.debug(f"Drawing text: {game['summary']}")
                    draw.text((10, 10 + i * fontSize), game['summary'], font=font, fill = 0)
                logging.debug("Updating display")
                epd.display_Partial(epd.getbuffer(Himage),0, 0, epd.width, epd.height)
                previousSchedule = schedule
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

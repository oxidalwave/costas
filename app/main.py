#!/usr/bin/python
# -*- coding:utf-8 -*-
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

def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("epd7in5_V2 Demo")
        epd = epaper.epaper('epd7in5_V2').EPD()
        
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        while (True):
            logging.info("Drawing clock...")
            epd.init_fast()
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            schedule = statsapi.schedule(start_date='07/01/2018',end_date='07/31/2018',team=143,opponent=121)
            for i, game in enumerate(schedule):
                draw.text((10 * i, 120), f"{game['game_date']} Game {game['game_num']} - WP: {game['winning_pitcher']}, LP; {game['losing_pitcher']}", font = font24, fill = 0)
            epd.display_Partial(epd.getbuffer(Himage),0, 0, epd.width, epd.height)
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epaper.epaper('epd7in5_V2').epdconfig.module_exit(cleanup=True)
        exit()

if __name__ == "__main__":
    main()

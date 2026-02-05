#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
import epaper
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epaper.epaper('epd7in5b_V2').EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype('Font.ttc', 24)
    font18 = ImageFont.truetype('Font.ttc', 18)
    font35 = ImageFont.truetype('Font.ttc', 35)

    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...")
    epd.init_fast()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    draw.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
    draw.text((150, 0), u'微雪电子', font = font24, fill = 0)
    draw.line((20, 50, 70, 100), fill = 0)
    draw.line((70, 50, 20, 100), fill = 0)
    draw.rectangle((20, 50, 70, 100), outline = 0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    time.sleep(2)

    # partial update
    logging.info("5.show time")
    epd.init_part()
    # Himage = Image.new('1', (epd.width, epd.height), 0)
    # draw = ImageDraw.Draw(Himage)
    num = 0
    while (True):
        draw.rectangle((10, 120, 130, 170), fill = 255)
        draw.text((10, 120), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.display_Partial(epd.getbuffer(Himage),0, 0, epd.width, epd.height)
        num = num + 1
        if(num == 10):
            break

    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.error(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit(cleanup=True)
    exit()

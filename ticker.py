#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ticker.py

import os
import requests, json
import multiprocessing

from lomond import WebSocket
from lomond.persist import persist

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=5, block_orientation=-90, rotate=2)
lightBright = 2
device.contrast(lightBright * 16)
minute = 1


def info(title):
    print(title)

if __name__ == '__main__':
    info("__Main__")

    websocket = WebSocket('wss://ws-feed.gdax.com')

    for event in persist(websocket):
        try:
            if event.name == "ready":
                websocket.send_json(
                    type='subscribe',
                    product_ids=['BTC-USD'],
                    channels=['ticker']
                )
            elif event.name == "text":
                x = json.loads(event.text)
                if 'price' in x:
                    priceFloat = float(x["price"])
                    info(priceFloat)
                    price = int(priceFloat)
                    with canvas(device) as draw:
                        text(draw, (9, 0), "$" + str(price), fill="white", font=proportional(LCD_FONT))
        except:
            info('error handling %r', event)
            websocket.close()

#!/usr/bin/env python3
"""
Notification script to send data through NBP TrackAddict protocol.
"""

import argparse
import asyncio
import time
from collections import OrderedDict
import logging
import queue

import aiofiles
from pynbp import NbpPayload, NbpKPI, WifiPyNBP

LOGGER = logging.Logger(__name__)


class EventHandler():
    def __init__(self, queue: queue.Queue, path: str):
        self.path = path
        self.nbp_queue = queue
        self.header = None

    async def read_file_header(self, f):
        header, units = None, None
        while True:
            line = await f.readline()
            if len(line) == 0:
                LOGGER.warning("Skip")
                continue
            if line.startswith("Time"):
                header = line
            if line.strip().startswith("sec"):
                units = line
            if header is not None and units is not None:
                break

        await self.process_header(header, units)

    async def process_header(self, header, units):
        self.header = OrderedDict([
            (h.strip(), u.strip())
            for h, u in zip(header.split("\t")[1:], units.split("\t")[1:])
        ])

    async def process_lines(self):
        async with aiofiles.open(self.path) as f:
            await self.read_file_header(f)
            f.seek(-1, 2)
            LOGGER.warning("File header read.")
            while True:
                line = await f.readline()
                if len(line) == 0:
                    continue
                values = line.split("\t")
                packets = [
                    NbpKPI(name=header[0], unit=header[1], value=value.strip())
                    for (header, value) in zip(self.header.items(), values[1:])
                ]
                self.nbp_queue.put(NbpPayload(
                    timestamp=time.time(), packettype="UPDATE", nbpkpilist=packets))


def argument_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("logfile", help="Software logfile.")
    parser.add_argument("-ip", type=str, default="0.0.0.0",
                        help="Address ip to bind the nbp server.")
    parser.add_argument("-p", "--port", type=int, default=35000,
                        help="Server port.")
    parser.add_argument("-u", "--update", type=float, default=0.2,
                        help="Update interval for the server.")
    return parser.parse_args()


def main():
    args = argument_parser()
    LOGGER.warning(
        "Start Wifi NBP server on: {}:{}".format(args.ip, args.port))
    nbp_queue = queue.Queue()
    nbp_srv = WifiPyNBP(nbp_queue, ip=args.ip, port=args.port,
                        min_update_interval=args.update)
    nbp_srv.daemon = True
    nbp_srv.start()
    LOGGER.warning("NBP server started.")
    nbp_queue.put(
        NbpPayload(timestamp=time.time(), packettype='ALL', nbpkpilist=[])
    )
    loop = asyncio.new_event_loop()
    event_handler = EventHandler(nbp_queue, args.logfile)
    loop.run_until_complete(event_handler.process_lines())


if __name__ == "__main__":
    main()

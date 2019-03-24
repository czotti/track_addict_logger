import argparse
from collections import OrderedDict
import logging
import pyinotify
import queue
import time
from pynbp import NbpPayload, NbpKPI, WifiPyNBP

LOGGER = logging.Logger(__name__)


def callback(notifier):
    print(notifier)
    return False


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, queue: queue.Queue, path: str):
        self.file = open(path, 'r')
        self.nbp_queue = queue
        self.read_file_lines()
        self.header = None

    def read_file_lines(self):
        header, units = None, None
        lines = iter(self.file.readlines())
        for line in lines:
            if line.startswith("Time"):
                header = line
            if line.strip().startswith("sec"):
                units = line
            if header is not None and units is not None:
                break

        self.process_header(header, units)
        self.process_lines(lines)

    def process_header(self, header, units):
        self.header = OrderedDict([
            (h.strip(), u.strip())
            for h, u in zip(header.split("\t")[1:], units.split("\t")[1:])
        ])

    def process_lines(self, lines):
        for line in lines:
            values = line.split("\t")
            packets = [
                NbpKPI(name=header[0], unit=header[1], value=value.strip())
                for (header, value) in zip(self.header.items(), values[1:])
            ]
            self.nbp_queue.put(NbpPayload(
                timestamp=time.time(), packettype="UPDATE", nbpkpilist=packets))

    def process_IN_CLOSE_WRITE(self, event):
        self.process_lines(self.file.readlines())


def argument_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("logfile", help="Software logfile.")
    parser.add_argument("-ip", type=str, default="0.0.0.0",
                        help="Adress ip to bind the nbp server.")
    parser.add_argument("-p", "--port", type=int, default=35000,
                        help="Port for the server to listen.")
    parser.add_argument("-u", "--update", type=float, default=0.2,
                        help="Update interval for the server.")
    return parser.parse_args()


def main():
    args = argument_parser()
    LOGGER.warning("Start Wifi NBP server on: {}:{}".format(args.ip, args.port))
    nbp_queue = queue.Queue()
    nbp_srv = WifiPyNBP(nbp_queue, ip=args.ip, port=args.port, min_update_interval=args.update)
    nbp_srv.daemon = True
    nbp_srv.start()
    LOGGER.warning("NBP server started.")
    nbp_queue.put(
        NbpPayload(timestamp=time.time(), packettype='ALL', nbpkpilist=[])
    )
    time.sleep(5)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler(nbp_queue, args.logfile))
    wm.add_watch(args.logfile, pyinotify.IN_CLOSE_WRITE)
    notifier.loop()

if __name__ == "__main__":
    main()
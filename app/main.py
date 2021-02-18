#!/usr/bin/env python3

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def parse_edid():
    return sys.stdin.read().strip().lower().replace(' ', '').replace('\n', '')


def print_cmd(edid):
    print('readonly EDID="/home/ustreamer/edids/tc358743-edid.hex"')
    print('echo -ne "" | sudo tee "${EDID}" && \\')
    max_chars = 40
    for i in range(int(len(edid) / max_chars) + 1):
        start = i * max_chars
        end = start + max_chars
        snippet = edid[start:end]
        print('  echo \'%s\' | sudo tee -a "${EDID}" && \\' % snippet)
    print('  sudo v4l2-ctl --device=/dev/video0 --set-edid=file="${EDID}" '
          '--fix-edid-checksums')


def main(args):
    configure_logging()
    logger.info('Started runnning')
    print_cmd(parse_edid())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Make EDID',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    main(parser.parse_args())

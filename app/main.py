#!/usr/bin/env python3

import argparse
import binascii
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


def read_input(input, binary):
    if not input:
        return sys.stdin.read()
    mode = 'r'
    if binary:
        mode += 'b'
    with open(input, mode) as infile:
        return infile.read()


def parse_hex_edid(input_raw):
    return input_raw.strip().lower().replace(' ', '').replace('\n', '')


def parse_binary_edid(input_raw):
    return binascii.hexlify(input_raw).decode('ascii')


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


def print_yaml(edid):
    print('ustreamer_edid: |')
    max_chars = 60
    for i in range(int(len(edid) / max_chars) + 1):
        start = i * max_chars
        end = start + max_chars
        snippet = edid[start:end]
        print('  %s' % snippet)


def main(args):
    configure_logging()
    logger.info('Started runnning')
    input_raw = read_input(args.input, args.binary)
    if args.binary:
        edid = parse_binary_edid(input_raw)
    else:
        edid = parse_hex_edid(input_raw)
    if args.yaml:
        print_yaml(edid)
    else:
        print_cmd(edid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Make EDID',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', default=None)
    parser.add_argument('-b', '--binary', dest='binary', action='store_true')
    parser.set_defaults(binary=False)
    parser.add_argument('--yaml', dest='yaml', action='store_true')
    parser.set_defaults(yaml=False)
    main(parser.parse_args())

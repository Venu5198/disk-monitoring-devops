#!/usr/bin/env python3

import argparse
import shutil
import logging
import sys


LOG_FILE = "disk_usage.log"


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Disk usage check")
    parser.add_argument("--path", required=True)
    parser.add_argument("--threshold", type=int, required=True)
    return parser.parse_args()


def main():
    setup_logging()

    try:
        args = parse_args()

        total, used, free = shutil.disk_usage(args.path)
        usage = int((used / total) * 100)

        message = f"Disk usage for {args.path} is {usage}%"
        print(message)
        logging.info(message)

        if usage >= args.threshold:
            print("Status: CRITICAL")
            logging.warning("Status CRITICAL")
            sys.exit(1)

        print("Status: OK")
        logging.info("Status OK")
        sys.exit(0)

    except Exception as e:
        logging.error(f"Script failure: {e}")
        print(f"Script failure: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
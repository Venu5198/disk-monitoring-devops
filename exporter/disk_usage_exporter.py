#!/usr/bin/env python3

import time
import shutil
import argparse
from prometheus_client import start_http_server, Gauge


disk_usage_percent = Gauge(
    "disk_usage_percent",
    "Disk usage percentage",
    ["path"]
)

disk_total_bytes = Gauge(
    "disk_usage_total_bytes",
    "Total disk size in bytes",
    ["path"]
)

disk_free_bytes = Gauge(
    "disk_usage_free_bytes",
    "Free disk space in bytes",
    ["path"]
)


def parse_args():
    parser = argparse.ArgumentParser(description="Disk usage Prometheus exporter")
    parser.add_argument("--path", required=True)
    parser.add_argument("--port", type=int, default=9105)
    parser.add_argument("--interval", type=int, default=30)
    return parser.parse_args()


def collect(path):
    total, used, free = shutil.disk_usage(path)
    usage = (used / total) * 100

    disk_usage_percent.labels(path=path).set(round(usage, 2))
    disk_total_bytes.labels(path=path).set(total)
    disk_free_bytes.labels(path=path).set(free)


def main():
    args = parse_args()

    start_http_server(args.port)
    print(f"Exporter running on port {args.port}")

    while True:
        collect(args.path)
        time.sleep(args.interval)
        

if __name__ == "__main__":
    main()
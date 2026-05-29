#!/usr/bin/env python3
import sys
from pathlib import Path

from rosbags.highlevel import AnyReader


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/inspect_rosbag_topics.py /path/to/file.bag")
        return 2

    bag_path = Path(sys.argv[1]).expanduser().resolve()
    if not bag_path.exists():
        print(f"ERROR: bag does not exist: {bag_path}")
        return 1

    print(f"bag_path: {bag_path}")
    print(f"bag_size_mb: {bag_path.stat().st_size / 1_000_000:.1f}")

    with AnyReader([bag_path]) as reader:
        duration_s = (reader.end_time - reader.start_time) / 1e9
        print(f"start_time_ns: {reader.start_time}")
        print(f"end_time_ns: {reader.end_time}")
        print(f"duration_s: {duration_s:.3f}")
        print("topics:")
        for conn in sorted(reader.connections, key=lambda c: c.topic):
            print(f"  {conn.topic} | {conn.msgtype}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

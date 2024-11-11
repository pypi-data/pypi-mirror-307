#!/usr/bin/env python3

from pons.event_log import *

e = load_event_log()

for ts, events in e.items():
    print(ts, len(events))
block = get_events_in_range(e, 3599, 3600.0, filter_in=["NET"])

print("events in last block:", len(block))

print(block)

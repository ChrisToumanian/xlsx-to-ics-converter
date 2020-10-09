#!/usr/bin/python3

from ics import Calendar, Event

calendar = Calendar()

def add_event(name, begin, end, all_day):
    global calendar
    e = Event()
    e.name = name
    e.begin = begin
    e.end = end
    if all_day:
        e.make_all_day()
    calendar.events.add(e)

def create_ics(filename):
    global calendar
    with open(filename, 'w') as f:
        f.writelines(calendar)

#!/usr/bin/python3 
import sys
import pytz
from datetime import datetime, timedelta
import makecalendar

employees = []
csv_filename = ""
label = ""
data = []
ics_filename = "calendar.ics"
events = []

class Event:
    name = ""
    employee = ""
    begin = None
    end = None
    off = False
    sick = False
    vacation = False
    on_call = False

def read_args():
    global employees
    global csv_filename
    global ics_filename
    global label

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-i": # input csv
            csv_filename = sys.argv[i+1]
        elif sys.argv[i] == "-e": # add employee
            employees.append(sys.argv[i+1])
        elif sys.argv[i] == "-o": # output ics
            ics_filename = sys.argv[i+1]
        elif sys.argv[i] == "-l": # label
            label = sys.argv[i+1]

def read_csv():
    global csv_filename
    global data
    
    # Read rows of schedule
    rows = []
    with open(csv_filename) as f:
        rows = f.readlines()
    rows = [x.strip() for x in rows]

    # Create matrix from row data
    h = len(rows)
    data = [0]*h
    for y in range(h):
        data[y] = rows[y].split(",")

def find_month(text):
    if "JANUARY" in text: return 1
    elif "FEBRUARY" in text: return 2
    elif "MARCH" in text: return 3
    elif "APRIL" in text: return 4
    elif "MAY" in text: return 5
    elif "JUNE" in text: return 6
    elif "JULY" in text: return 7
    elif "AUGUST" in text: return 8
    elif "SEPTEMBER" in text: return 9
    elif "OCTOBER" in text: return 10
    elif "NOVEMBER" in text: return 1
    elif "DECEMBER" in text: return 12
    return 0

def find_employee(text):
    for employee in employees:
        if employee in text:
            return employee
    return 0

def convert_time(time):
    time = time.replace("a", "AM")
    time = time.replace("p", "PM")
    if ":" in time:
        return datetime.strptime(time, '%I:%M%p')
    else:
        return datetime.strptime(time, '%I%p')

def parse_data():
    global data
    global employees
    global events
    year = 2020
    month = 1
    employee = ""
    days = []

    for y in range(len(data)):
        if find_month(data[y][0]): # Find month
            month = find_month(data[y][0])
            days = data[y+1]
        elif find_employee(data[y][0]): # Find employee
            employee = find_employee(data[y][0])
            times = data[y]

            # Add event for each day in row
            for x in range(len(days)):
                ev = Event()
                ev.employee = employee

                # Break if no date set
                if days[x] != "":

                    # Set date
                    ev.begin = datetime(year, month, int(days[x]))
                    local = pytz.timezone("America/Los_Angeles")

                    # Handle flags
                    if "OFF" in times[x]:
                        ev.off = True
                        ev.name = ev.employee + " (OFF)"
                    elif "SICK" in times[x]:
                        ev.sick = True
                        ev.name = ev.employee + " (SICK)"
                    elif "VAC" in times[x]:
                        ev.vacation = True
                        ev.name = ev.employee + " (VAC)"
                    elif "OC" in times[x]:
                        ev.on_call = True
                        ev.name = ev.employee + " (OC)"
                    else:
                        ev.name = ev.employee

                        # Set date
                        begin_time = convert_time(times[x].split("-")[0])
                        end_time = convert_time(times[x].split("-")[1])
                        ev.begin = datetime(year, month, int(days[x]), begin_time.hour, begin_time.minute, begin_time.second)
                        ev.end = datetime(year, month, int(days[x]), end_time.hour, end_time.minute, end_time.second)
                        
                        # If end before begin, advance day
                        if ev.end < ev.begin:
                            ev.end = ev.end + timedelta(days=1)
                        ev.end = local.localize(ev.end, is_dst=None).astimezone(pytz.utc)

                    # Set timezone
                    ev.begin = local.localize(ev.begin, is_dst=None).astimezone(pytz.utc)

                    # Add to events
                    events.append(ev)

def create_calendar():
    global events
    global ics_filename
    global label

    if label is not "":
        label += " ";

    for ev in events:
        if not ev.off and not ev.vacation and not ev.sick and not ev.on_call:
            print(label + ev.name, ev.begin.strftime('%Y-%m-%d %H:%M:%S'), ev.end.strftime('%Y-%m-%d %H:%M:%S'))
            makecalendar.add_event(label + ev.name, ev.begin.strftime('%Y-%m-%d %H:%M:%S'), ev.end.strftime('%Y-%m-%d %H:%M:%S'), False)
        elif not ev.off:
            print(label + ev.name, ev.begin.strftime('%Y-%m-%d %H:%M:%S'))
            makecalendar.add_event(label + ev.name, ev.begin.strftime('%Y-%m-%d %H:%M:%S'), ev.begin.strftime('%Y-%m-%d %H:%M:%S'), True)

    makecalendar.create_ics(ics_filename)

def main():
    read_args()
    read_csv()
    parse_data()
    create_calendar()

main()

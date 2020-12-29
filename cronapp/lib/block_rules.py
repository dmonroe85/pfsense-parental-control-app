import datetime as dt
import json, time

import requests

from lib.util import get_minutes
from lib.config import G_SHEET_KEY
from lib.constants import weekday_lkup, MAX_HOUR

def read_google_sheet(sheet=None):
    key = G_SHEET_KEY
    url = 'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv'.format(key)
    
    if sheet is not None:
        url = url + '&sheet={}'.format(sheet)

    response = requests.get(url)

    rows = iter([
        [y.rstrip('"').lstrip('"') for y in x.split(',')]
        for x in response.text.split('\n')
    ])

    headers = next(rows)

    data = [ dict(zip(headers, row)) for row in rows ]
        
    return data

def within_schedule(t):
    t_dow = t.weekday()
    t_minutes = t.hour * 60 + t.minute

    def f(row):
        start = get_minutes(row['Start'])
        end = get_minutes(row['End'])
        days = set([
            weekday_lkup[d.strip().lower()] for d in row['Days'].split(';')
        ])

        overnight = end < start

        schedule = {}
        for d in days:
            d_tomorrow = (d + 1) % 7
            if d not in schedule:
                schedule[d] = []

            if d_tomorrow not in schedule:
                schedule[d_tomorrow] = []

            if overnight:
                schedule[d].append([start, MAX_HOUR])
                schedule[d_tomorrow].append([0, end])
            else:
                schedule[d].append([start, end])

        for s in schedule.get(t_dow, []):
            if s:
                sched_start, sched_end = s
                if sched_start <= t_minutes <= sched_end:
                    return True

        return False

    return f

def block_reason(row):
    if row['Disabled']:
        return 'Disabled'

    elif row['Scheduled_Block']:
        return row['Schedule']

    print(row)
    raise Exception("There should be a reason if we are blocking")

def string_to_bool(v):
    return v.strip().lower() in ['true', 't']

class ActiveFilters(object):
    def __init__(self, device_lkup, overrides):
        self.seen_user = set()
        self.seen_mac = set()
        self.filters = []
        self.device_lkup = device_lkup

        self.overrides = {}

        current_millis = int(time.time() * 1000)
        for user, ov_obj in overrides.items():
            start_date = ov_obj.get('startDate', 0)
            end_date = ov_obj.get('endDate', 0)

            within_time = (start_date < current_millis < end_date)
            action = ov_obj.get('action')

            if action is None or not within_time:
                continue

            self.overrides[user] = action

    def add_devices(self, user, manual_disable, scheduled_disable, schedule='NotARealSchedule'):
        disabled = manual_disable or scheduled_disable
        if not disabled:
            return
        
        if user in self.seen_user:
            return

        self.seen_user.add(user)

        reason = block_reason({
            'Disabled': manual_disable,
            'Scheduled_Block': scheduled_disable,
            'Schedule': schedule
        })

        for device in self.device_lkup.get(user, []):
            descr = device['Description']
            mac = device['MAC']

            if mac in self.seen_mac:
                continue

            self.filters.append({
                'User': user,
                'Reason': reason,
                'Description': descr,
                'MAC': mac
            })

            self.seen_mac.add(mac)

    def add_unknown_devices(self, network_devices):
        known_devices = \
            set([d['MAC'] for _, devices in self.device_lkup.items() for d in devices])

        for mac in network_devices:
            if mac not in known_devices:
                self.filters.append({
                    'User': 'Unknown',
                    'Reason': 'UnknownDevice',
                    'Description': mac,
                    'MAC': mac
                })

    def apply_overrides(self):
        new_filters = [
            f for f in self.filters
            if self.overrides.get(f['User']) != 'ALLOWED'
        ]

        for user, action in self.overrides.items():
            if action == 'BLOCKED':
                for device in self.device_lkup.get(user, []):
                    descr = device['Description']
                    mac = device['MAC']

                    new_filters.append({
                        'User': user,
                        'Reason': 'Override',
                        'Description': descr,
                        'MAC': mac
                    })

        self.filters = new_filters


def find_blocked(network_devices, overrides):
    timestamp = dt.datetime.now()

    print('Getting google sheets')
    schedules = dict(
        (r['Schedule'], {**r, 'Scheduled_Block': within_schedule(timestamp)(r) })
        for r in read_google_sheet('Schedules')
    )
    users = \
        dict(
            (r['User'], string_to_bool(r['Disabled']))
            for r in read_google_sheet('Users')
        )
    rules = read_google_sheet('Rules')
    devices = [
        {**r, 'MAC': r['MAC'].strip().lower() }
        for r in read_google_sheet('Devices')
        if r['MAC'].strip()
    ]

    device_lkup = {}
    for d in devices:
        user = d['User']
        if user not in device_lkup:
            device_lkup[user] = []

        device_lkup[user].append(d)

    active_filters = ActiveFilters(device_lkup, overrides)
    for r in rules:
        user = r['User']
        schedule = r['Schedule']

        manual_disable = users.get(user, False)
        scheduled_disable = schedules.get(schedule, {}).get('Scheduled_Block', False)

        active_filters.add_devices(user, manual_disable, scheduled_disable, schedule)

    for u, d in users.items():
        active_filters.add_devices(u, d, False)

    active_filters.add_unknown_devices(network_devices)

    active_filters.apply_overrides()

    return active_filters.filters
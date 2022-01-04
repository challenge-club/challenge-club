import datetime
import time

import strictyaml


BAR_SCALE = 3


def get_data():
    return strictyaml.load(open('2021-01_training/trained.yaml').read()).data


def get_minutes(lines):
    return [get_minutes_part(line) for line in lines.values()]


def get_minutes_part(line):
    if not line:
        return None
    return int(line.split(', ')[-1])


def make_sparkline(minutes):
    return ''.join(make_bar(minute) for minute in minutes)


def make_bar(height):
    height_ = height // BAR_SCALE if height else 0
    return f'<div class="bar" style="height: {height_}px"></div>'


def get_main_html():
    start = time.monotonic()
    html = '<table class="bordered">\n\n'

    trainings = get_data()
    today = int(datetime.datetime.now().strftime('%d'))

    counters = {person: len([line for line in lines.values() if line]) for person, lines in trainings.items()}

    html += '<tr><th style="border: 0"></th>' + ''.join(f'<th>{person} &middot; {counters[person]}</th>' for person in trainings) + '</tr>\n\n'

    minutes = {person: get_minutes(lines) for person, lines in trainings.items()}
    max_minutes = max(max(x for x in m if x is not None) for m in minutes.values())
    strut_bar = f'<div class="bar" style="height: {max_minutes // BAR_SCALE}px; width: 0;"></div>'
    sparklines = {person: make_sparkline(minutes[person]) for person in trainings}
    html += f'<tr><td style="border: 0"></td>' + ''.join(f'<td class="centered">{strut_bar}{sparklines[person]}</td>' for person in trainings) + '</tr>\n\n'

    for date_num in range(1, min(31, today) + 1):
        date = f'{date_num:02d}'
        html += f'<tr><td>{date}</td>'
        for person in trainings:
            training = trainings[person][date] if date in trainings[person] else ''
            html += f'<td>{training}</td>'
        html += '</tr>\n\n'

    html += '</table>'

    print(f"▓ Done in {time.monotonic() - start:.1f} seconds")
    return html


# todo: sparklines

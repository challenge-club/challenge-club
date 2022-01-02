import datetime
import time

import strictyaml


def get_data():
    return strictyaml.load(open('2021-01_training/trained.yaml').read()).data


def get_main_html():
    start = time.monotonic()
    html = '<table class="bordered">\n\n'

    trainings = get_data()
    today = int(datetime.datetime.now().strftime('%d'))

    html += '<tr><th style="border: 0"></th>' + ''.join(f'<th>{person} &middot; {len(trainings[person])}</th>' for person in trainings) + '</tr>\n\n'

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

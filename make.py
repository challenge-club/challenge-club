import os
from importlib import import_module

latest = import_module('2021-01_training.trained')


dnames = sorted(d for d in os.listdir('.') if d.startswith('ch_202'))


def make_menu():
    links = [dname[3:] for dname in dnames]
    return ' &middot; '.join(links)


html = open('template.html').read()

params = {
    'title': 'Спортивный клуб января',
    'menu': make_menu(),
    'body': latest.get_main_html(),
}

for param, value in params.items():
    html = html.replace('{{' + param + '}}', value)
open('index.html', 'w').write(html)

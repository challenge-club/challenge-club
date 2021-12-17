import collections
import time

import strictyaml


def get_eat_data():
    return strictyaml.load(open('eaten.yaml').read()).data


def get_header():
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Овощной клуб декабря</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans+Condensed:wght@300&display=swap" rel="stylesheet">
<style>
    * {font-family: 'Open Sans Condensed', sans-serif; color: #444;}
    body {padding: 1rem; font-size: 1.9vmin;}
    div.products {padding: 0.4rem 0 1rem 2rem; line-height: 110%;}
    h3 {color: #888; margin: 0;}
    h3 * {font-family: sans-serif;}
    span.total_count {font-weight: normal;}
    span.counter {color: #aaa; font-size: 64%;}
    .missed {color: #3333ff;}
    .eaten {color: #ddd;}
    .unique {color: orange;}
    div.all_products {margin-top: 3rem; border-top: 1px solid #ddd; padding-top: 1rem; line-height: 110%;}
    sup {color: inherit; font-variant: small-caps; font-size: 55%;}
</style>
</head>
<body>

<script>

function highlights(person) {
    var links = document.querySelectorAll('span.missed_by_' + person);
    links.forEach(function(link){
        link.classList.add('missed') 
    });
    var links = document.querySelectorAll('span.eaten_by_' + person);
    links.forEach(function(link){
        link.classList.add('eaten') 
    });
    var links = document.querySelectorAll('span.unique_by_' + person);
    links.forEach(function(link){
        link.classList.add('unique') 
    });
}

function go_dull() {
    var links = document.querySelectorAll('span.missed');
    links.forEach(function(link){
        link.classList.remove('missed')
    });
    var links = document.querySelectorAll('span.eaten');
    links.forEach(function(link){
        link.classList.remove('eaten')
    });
    var links = document.querySelectorAll('span.unique');
    links.forEach(function(link){
        link.classList.remove('unique')
    });
}

</script>
"""


def get_css_classes(product, eaten, eaten_set, unique_set):
    css_classes = []
    for person in eaten:
        if product in eaten_set[person]:
            css_classes.append(f'eaten_by_{person}')
        else:
            css_classes.append(f'missed_by_{person}')
        if product in unique_set[person]:
            css_classes.append(f'unique_by_{person}')
    return ' '.join(css_classes)


def union_sets(sets):
    result = set()
    for s in sets:
        result.update(s)
    return result


def get_main_html():
    start = time.monotonic()

    eaten = get_eat_data()
    eaten_set = {p: set(e) for p, e in eaten.items()}

    all_products = set("""
апельсин красный
банан красный
бергамот
капуста романеско
капуста цветная фиолетовая
лук белый
лук-порей
патиссон
сельдерей корень
слива синяя
слива жёлтая
базилик
тимьян
мелисса
майоран
""".strip().splitlines())
    for products in eaten_set.values():
        all_products.update(products)

    eaten_by_others_set = {p: union_sets(eaten_set[x] for x in eaten if x != p) for p in eaten}
    unique_set = {p: e - eaten_by_others_set[p] for p, e in eaten_set.items()}

    html = get_header()
    sorting = [(-len(eaten[person]), person) for person in eaten]
    sorting.sort()

    for _count, person in sorting:
        count = -_count
        print(f"{person}... ", end='', flush=True)
        if count != len(eaten_set[person]):
            counter = collections.Counter(eaten[person])
            raise Exception(f"Duplicates in product list of {person}: {[x for x in eaten_set[person] if counter[x] > 1]}")

        section = f'''<div><h3><span onmouseover="highlights('{person}')" onmouseout="go_dull()">{person} <span class="total_count">&middot; {count}</span></span></h3><div class="products">\n'''
        products = []

        for i, product in enumerate(eaten[person]):
            products.append(f'\n<nobr><span class="counter">{i + 1}</span> <span class="{get_css_classes(product, eaten, eaten_set, unique_set)}">{product}</span></nobr>')

        section += ' <span class="sep">&middot;</span> '.join(products)
        section += '\n</div></div>\n\n'
        html += section
        print('ok')

    html += '<div class="all_products">'

    products = []
    for product in sorted(all_products):
        marks = ''.join(name[0] for name in sorted(eaten.keys()) if product in eaten_set[name])
        products.append(f'<nobr><span class="{get_css_classes(product, eaten, eaten_set, unique_set)}">{product}<sup>{marks}</sup></span></nobr>')
    html += ' &middot; \n'.join(products)

    html += f'<br><br>все вместе: {len(union_sets(eaten_set.values()))}</div></body>'

    print('unique:', {p: len(e) for p, e in unique_set.items()})
    print(f"▓ Done in {time.monotonic() - start:.1f} seconds")
    return html


if __name__ == '__main__':
    open('index.html', 'w').write(get_main_html())

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
    body {padding: 1rem;}
    div.products {padding: 0.4rem 0 1rem 2rem;}
    h3 {color: #888; margin: 0;}
    h3 * {font-family: sans-serif;}
    span.total_count {font-weight: normal;}
    span.counter {color: #aaa; font-size: 80%;}
    .missed {color: #3333ff;}
    .eaten {color: #ddd;}
    .unique {color: orange;}
    div.all_products {margin-top: 3rem; border-top: 1px solid #ddd; padding-top: 1rem;}
    sup {color: inherit;}
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


def get_css_classes(product):
    eaten = get_eat_data()
    css_classes = []
    for person in eaten:
        if product in eaten[person]:
            css_classes.append(f'eaten_by_{person}')
            if all(product not in eaten[p] for p in eaten if p != person):
                css_classes.append(f'unique_by_{person}')
        else:
            css_classes.append(f'missed_by_{person}')
    return ' '.join(css_classes)


def get_main_html():
    eaten = get_eat_data()
    html = get_header()
    sorting = [(-len(eaten[person]), person) for person in eaten]
    sorting.sort()

    for _, person in sorting:
        if len(eaten[person]) != len(set(eaten[person])):
            raise Exception(f"Duplicates in product list of {person}!")

        section = f'''<div><h3><span onmouseover="highlights('{person}')" onmouseout="go_dull()">{person} <span class="total_count">&middot; {len(eaten[person])}</span></span></h3><div class="products">\n'''
        products = []

        for i, product in enumerate(eaten[person]):
            products.append(f'\n<nobr><span class="counter">{i + 1}</span> <span class="{get_css_classes(product)}">{product}</span></nobr>')

        section += ' <span class="sep">&middot;</span> '.join(products)
        section += '\n</div></div>\n\n'
        html += section

    html += '<div class="all_products">'
    all_products = set("""
апельсин красный
арбуз
базилик
баклажан
брусника
брюква
виноград жёлтый
виноград красный
виноград чёрный
вишня
водоросль ламинария
грейпфрут белый
грейпфрут красный
груша жёлтая
груша зелёная
гуайява
дыня желтая
дыня зелёная
земляника
имбирь
инжир
кабачок
цуккини
капуста кале
капуста китайская
капуста романеско
капуста цветная
картофель фиолетовый
клюква
кокос
кольраби
лайм
лук жёлтый
лук фиолетовый
лук-порей
манго
мангольд
морковь белая
морковь фиолетовая
облепиха
оливка зелёная
оливка розовая
оливка тёмно-розовая
оливка чёрная
паприка белая
паприка зелёная
паприка оранжевая
пастернак
патиссон
помидор зелёный
помидор красный
помидор розовый
редис белый
редис красный
ростки люцерны
руккола
салат листовой
свити
свёкла
свёкла жёлтая
слива синяя
слива жёлтая
смородина красная
смородина чёрная
спаржа
тыква
фенхель
финик
черешня
""".strip().splitlines())
    for products in eaten.values():
        all_products.update(products)
    products = []
    for product in sorted(all_products):
        marks = ''.join(name[0] for name in sorted(eaten.keys()) if product in eaten[name])
        products.append(f'<span class="{get_css_classes(product)}">{product}<sup>{marks}</sup></span>')
    html += ' &middot; \n'.join(products)

    html += '</div></body>'
    return html


if __name__ == '__main__':
    open('index.html', 'w').write(get_main_html())

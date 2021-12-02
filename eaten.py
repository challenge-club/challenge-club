import strictyaml


def get_eat_data():
    return strictyaml.load(open('eaten.yaml').read()).data


def get_header():
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Овощной клуб декабря</title>
<style>
    body {padding: 1rem;}
    div.products {padding: 0.4rem 0 1rem 2rem;}
    h3 {color: #888; margin: 0;}
    span.total_count {font-weight: normal;}
    span.counter {color: #aaa; font-size: 80%;}
    .highlighted {color: #3333ff;}
    .grayed {color: #ddd;}
    .unique {color: orange;}
</style>
</head>
<body>
<script>

function highlights(person) {
    var links = document.querySelectorAll('span.missed_by_' + person);
    links.forEach(function(link){
        link.classList.add('highlighted') 
    });
    var links = document.querySelectorAll('span.eaten_by_' + person);
    links.forEach(function(link){
        link.classList.add('grayed') 
    });
    var links = document.querySelectorAll('span.unique_by_' + person);
    links.forEach(function(link){
        link.classList.add('unique') 
    });
}

function go_dull() {
    var links = document.querySelectorAll('span.highlighted');
    links.forEach(function(link){
        link.classList.remove('highlighted')
    });
    var links = document.querySelectorAll('span.grayed');
    links.forEach(function(link){
        link.classList.remove('grayed')
    });
    var links = document.querySelectorAll('span.unique');
    links.forEach(function(link){
        link.classList.remove('unique')
    });
}

</script>
"""


def get_main_html():
    eaten = get_eat_data()
    html = get_header()
    sorting = [(-len(eaten[person]), person) for person in eaten]
    sorting.sort()

    for _, person in sorting:
        section = f'''<div><h3><span onmouseover="highlights('{person}')" onmouseout="go_dull()">{person} <span class="total_count">&middot; {len(eaten[person])}</span></span></h3><div class="products">\n'''
        products = []
        for i, product in enumerate(eaten[person]):
            css_class = ''
            for other_person in eaten:
                if other_person == person:
                    if all(product not in eaten[p] for p in eaten if p != person):
                        css_class += f' unique_by_{other_person}'
                else:
                    if product not in eaten[other_person]:
                        css_class += f' missed_by_{other_person}'
                    else:
                        css_class += f' eaten_by_{other_person}'
            products.append(f'\n<nobr><span class="counter">{i + 1}</span> <span class="eaten {css_class}">{product}</span></nobr>')
        section += ' <span class="sep">&middot;</span> '.join(products)
        section += '\n</div></div>\n\n'
        html += section

    return html


if __name__ == '__main__':
    open('index.html', 'w').write(get_main_html())

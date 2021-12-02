import strictyaml


def get_eat_data():
    return strictyaml.load(open('eaten.yaml').read()).data


def get_header():
    return """
<html>
<head>
<title>Овощной клуб декабря</title>
<style>
table {
    display: inline-block;
    margin-right: 1rem;
    border-collapse: collapse;
    vertical-align: top;
}
table td, table th {
    border: 1px solid #ddd;
    padding: 0.1rem 0.3rem;
}
th {
    color: #888;
}
span.total_count {
    font-weight: normal;
}
span.counter {
    color: #aaa;
    font-size: 80%;
}
.highlighted {
    color: #3333ff;
}
.grayed {
    color: #ddd;
}
</style>
</head>
<body>
<script>

function show_missing(person) {
    var links = document.querySelectorAll('span.missed_by_' + person);
    links.forEach(function(link){
        link.classList.add('highlighted') 
    });
    var links = document.querySelectorAll('span.eaten_by_' + person);
    links.forEach(function(link){
        link.classList.add('grayed') 
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
}

</script>
"""


def get_main_html():
    eaten = get_eat_data()
    html = get_header()

    for person in eaten:
        table = f'''<table onmouseover="show_missing('{person}')" onmouseout="go_dull()"><tr><th>{person} <span class="total_count">&middot; {len(eaten[person])}</span></th></tr>'''
        for i, product in enumerate(eaten[person]):
            css_class = ''
            for other_person in eaten:
                if other_person == person: continue
                if product not in eaten[other_person]:
                    css_class += f' missed_by_{other_person}'
                else:
                    css_class += f' eaten_by_{other_person}'
            table += f'<tr><td><span class="counter">{i + 1}</span> <span class="eaten {css_class}">{product}</span></td></tr>'
        table += '</table>'
        html += table

    return html


if __name__ == '__main__':
    print('saving...')
    open('index.html', 'w').write(get_main_html())

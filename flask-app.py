from flask import Flask

from eaten import get_main_html


app = Flask(__name__)

@app.route('/')
def main():
    return get_main_html()

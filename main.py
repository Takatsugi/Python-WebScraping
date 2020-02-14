from flask import Flask
from flask import jsonify
from scraping import scrape
from scraping import scrape_inside
from scraping import scrapeDailyKos
from scraping import scrapeDailyKosInside
from scraping import scrapeEverything

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(news=scrapeEverything())


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
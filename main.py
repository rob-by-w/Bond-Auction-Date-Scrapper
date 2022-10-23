import flask
from flask import Flask
from json import JSONEncoder, dumps
from datetime import date, datetime

import main_jgb
import main_ust

app = Flask(__name__)


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


@app.get("/")
def hello_world():
    return "Hello World"


@app.get("/jgb-auction-date")
def get_jgb_auction_date():
    jgb_auction_date = main_jgb.run()
    jgb_auction_date_list = [bond.__dict__ for bond in jgb_auction_date.values()]

    response = flask.jsonify(items=jgb_auction_date_list)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.get("/ust-auction-date")
def get_ust_auction_date():
    ust_auction_date = main_ust.run()

    response = flask.make_response(ust_auction_date.to_json(orient="records", date_format="iso"))
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

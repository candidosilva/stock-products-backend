from flask import Blueprint
import click
import json
import pandas as pd
from ..extentions.database import mongo

product = Blueprint("product", __name__)

@product.cli.command("import")
@click.argument("csvfile")
def inport_csv(csvfile):
    collection = mongo.db.produtos
    data = pd.read_csv(csvfile)
    jsondata = json.loads(data.to_json(orient='records'))
    collection.insert_many(jsondata)
    return collection.count

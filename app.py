import uuid
from flask import Flask, request
from db import stores, items

app = Flask(__name__)


@app.get("/store")
def get_all_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.post("/store")
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        return {"message": "Bad request. Ensure 'name', is inclued in the JSON payload."}, 400
    
    for store in stores.values():
        if store_data["name"] == store["name"]:
            return {"message": "Store already exists."}, 400

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201

@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()

    if "name" not in store_data:
        return {"message": "Bad request. Ensure 'name', is inclued in the JSON payload."}, 400

    if store_id in stores:
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
    else:
        return {"message": "Store not found"}, 404


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404


@app.post("/item")
def create_item():
    item_data = request.get_json()

    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        return {"message": "Bad request. Ensure 'price', 'store_id' and 'name' are inclued in the JSON payload."}, 400
    
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            return {"message": "Item already exists."}, 400

    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    if (
        "price" not in item_data
        or "name" not in item_data
    ):
        return {"message": "Bad request. Ensure 'price' and 'name' are inclued in the JSON payload."}, 400

    if item_id in items:
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item
    else:
        return {"message": "Item not found"}, 404


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        return {"message": "Item not found"}, 404
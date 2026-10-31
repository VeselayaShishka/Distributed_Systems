"""Lab 1 starter: reads work; students implement the three mutation routes.

Use one Waitress application thread. This intentionally process-local model is
not a concurrent or persistent storage implementation.
"""
import json
from dataclasses import field

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

from stories import STORY, STORY_KEY

from models import Book

app = Flask(__name__)
items = {}
next_id = 1
WRITABLE_FIELDS = {"name", "status", "category"}


class InputError(Exception):

    def __init__(self, code, message, status=400):
        self.code = code
        self.message = message
        self.status = status


def error(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status


@app.errorhandler(InputError)
def input_error(exc):
    return error(exc.code, exc.message, exc.status)


def parse_object():
    raw_body = request.get_data(as_text=True)
    print(repr(raw_body))
    if not request.is_json:
        raise InputError("unsupported_media_type", "Send a JSON request body.", 415)
    try:
        data = request.get_json()
    except BadRequest:
        raise InputError("invalid_json", "The request body is not valid JSON.")
    if not isinstance(data, dict):
        raise InputError("invalid_object", "The JSON body must be an object.")
    return data


def validate_item(data):
    allowed_fields = {"name", "status", "category"}

    unknown_fields = set(data.keys()) - allowed_fields
    if unknown_fields:
        raise InputError(
            "unknown_field",
            f"Unknown fields: {', '.join(sorted(unknown_fields))}."
        )

    name = validate_field(data.get("name"), "name")

    status = validate_field(data.get("status"), "status")
    if status not in STORY['statuses']:
        raise InputError("invalid_status", f"The {status} field must be one of {STORY['statuses']}.")

    category = validate_field(data.get("category"), "category")

    return name, status, category

def validate_field(input, name):

    if input is None:
        raise InputError("missing_field", f"The {name} field is required.")
    if not isinstance(input, str):
        raise InputError("invalid_type", f"The {name} field must be a string.")

    validated = input.strip()

    if not validated:
        raise InputError("empty_field", f"The {name} field cannot be empty.")
    return validated

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "catalog-service", "story": STORY_KEY})


@app.get("/items")
def list_items():
    return jsonify([items[item_id].to_dict() for item_id in sorted(items)])


@app.get("/items/<int:item_id>")
def get_item(item_id):
    if item_id not in items:
        return error("not_found", "No item has this ID.", 404)
    return jsonify(items[item_id].to_dict())


@app.post("/items")
def create_item():
    try:
        data = parse_object()
        name, status, category = validate_item(data)
    except InputError as e:
        return error(e.code, e.message, e.status)

    book = Book(name, status, category)
    items[book.id] = book

    print(jsonify(book.to_dict()))

    return jsonify(book.to_dict()), 201

@app.put("/items/<int:item_id>")
def replace_item(item_id):
    if item_id not in items:
        return error("not_found", f"No item with ID: {item_id}.", 404)

    try:
        data = parse_object()
        name, status, category = validate_item(data)
    except InputError as e:
        return error(e.code, e.message, e.status)

    items[item_id].name = name
    items[item_id].status = status
    items[item_id].category = category

    return jsonify(items[item_id].to_dict()), 200

@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    item = items.pop(item_id, None)

    if item is None:
        return error("not_found", f"No item with ID: {item_id}.", 404)

    return '',204
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
    """An HTTP error caused by a request, not by application state."""

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
    """Parse JSON and distinguish unsupported media from invalid JSON.

    Call this before validating fields. No state is modified here.
    """
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
    """TODO: return the three validated, trimmed writable fields.

    Reject missing/unknown fields, client IDs, wrong types, empty name/category,
    and a status outside STORY['statuses']. Raise InputError on rejection.
    Do all validation before changing items or next_id.
    """

    if len(data) > 3:
        raise Exception("Object must contain only name, status and category fields")

    name = validate_field(data.get("name"))

    status = validate_field(data.get("status"))
    if status not in STORY['statuses']:
        raise ValueError("invalid_status", f"The {status} field must be one of {STORY['statuses']}.")

    category = validate_field(data.get("category"))

    return name, status, category

def validate_field(input):
    if input is None:
        raise InputError("missing_field", f"The {input} field is required.")
    validated = input.strip()
    if not validated:
        raise InputError("empty_field", f"The {validated} field cannot be empty.")
    if not isinstance(validated, str):
        raise InputError("invalid_type", f"The {validated} field must be a string.")
    return validated

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "catalog-service", "story": STORY_KEY})


@app.get("/items")
def list_items():
    return jsonify([items[item_id] for item_id in sorted(items)])


@app.get("/items/<int:item_id>")
def get_item(item_id):
    if item_id not in items:
        return error("not_found", "No item has this ID.", 404)
    return jsonify(items[item_id])


@app.post("/items")
def create_item():
    """TODO: validate, allocate one ID, store, and return the created item (201)."""
    try:
        data = parse_object()
        item = validate_item(data)
    except InputError as e:
        return error(e.code, e.message, e.status)

    book = Book(item[0], item[1], item[2])
    items[book.id] = book

    return jsonify(item), 201

@app.put("/items/<int:item_id>")
def replace_item(item_id):
    """TODO: replace writable fields of an existing item; keep its ID (200)."""
    return error("not_implemented", "Checkpoint 3: implement PUT /items/{id}.", 501)


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    """TODO: delete an existing item (204, empty body); absent means 404."""
    return error("not_implemented", "Checkpoint 3: implement DELETE /items/{id}.", 501)

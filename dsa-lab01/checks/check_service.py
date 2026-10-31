#!/usr/bin/env python3
"""Finite black-box checks for Lab 1; Python standard library only.

Run one stage at a time against your own service. These checks never reset the
service or delete somebody else's items. The create stage leaves its records
because DELETE is not yet required; the crud stage removes its own records.
"""

import argparse
import json
import sys
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROFILES = {
    "campus": ("open", "doing"),
    "greenhouse": ("healthy", "warning"),
    "library": ("available", "on_loan"),
}


class CheckFailure(Exception):
    pass


class Checks:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.passed = 0
        self.owned_ids = []

    def require(self, condition, message):
        if not condition:
            raise CheckFailure(message)
        self.passed += 1

    def call(self, method, path, payload=None, raw=None, content_type="application/json"):
        body = raw
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": content_type} if body is not None else {}
        req = Request(self.base_url + path, data=body, headers=headers, method=method)
        try:
            response = urlopen(req, timeout=5)
        except HTTPError as exc:
            response = exc
        except (URLError, TimeoutError) as exc:
            raise CheckFailure(f"Cannot reach {self.base_url}: {exc}")
        with response:
            data = response.read()
            status = response.code
            try:
                value = json.loads(data) if data else None
            except (ValueError, UnicodeDecodeError):
                raise CheckFailure(f"{method} {path}: expected JSON or an empty 204 body")
        return status, value, data

    def error(self, response, status, label):
        code, data, _ = response
        self.require(code == status, f"{label}: expected {status}, got {code}")
        self.require(isinstance(data, dict) and isinstance(data.get("error"), dict)
                     and isinstance(data["error"].get("code"), str)
                     and isinstance(data["error"].get("message"), str),
                     f"{label}: use the documented JSON error structure")

    def snapshot(self):
        code, data, _ = self.call("GET", "/items")
        self.require(code == 200 and isinstance(data, list), "GET /items must return a JSON array")
        return data

    def common(self):
        code, data, _ = self.call("GET", "/health")
        self.require(code == 200 and isinstance(data, dict) and data.get("status") == "ok"
                     and data.get("service") == "catalog-service", "Check the /health contract")
        story = data.get("story")
        self.require(story in PROFILES, "Health must identify campus, greenhouse, or library")
        self.story = story
        self.snapshot()

    def starter(self):
        self.require(self.snapshot() == [], "Starter stage expects a newly started, empty service")
        self.error(self.call("GET", "/items/999999999"), 404, "Missing-item read")
        sample = {"name": "Starter check", "status": PROFILES[self.story][0], "category": "check"}
        self.error(self.call("POST", "/items", sample), 501, "Unfinished POST")
        self.error(self.call("PUT", "/items/999999999", sample), 501, "Unfinished PUT")
        self.error(self.call("DELETE", "/items/999999999"), 501, "Unfinished DELETE")
        self.require(self.snapshot() == [], "Unfinished routes must not change state")

    def create(self):
        marker = "Lab check " + uuid.uuid4().hex[:10]
        self.sample = {"name": marker, "status": PROFILES[self.story][0], "category": "check"}
        padded = {key: f"  {value}  " for key, value in self.sample.items()}
        code, item, _ = self.call("POST", "/items", padded)
        self.require(code == 201 and isinstance(item, dict), f"POST expected 201 and an item, got {code}")
        item_id = item.get("id")
        self.require(type(item_id) is int and item_id > 0, "The server must allocate a positive integer ID")
        self.owned_ids.append(item_id)
        self.require(item == {"id": item_id, **self.sample}, "Created item must contain exactly the trimmed fields and ID")
        code, read_back, _ = self.call("GET", f"/items/{item_id}")
        self.require(code == 200 and read_back == item, "A successful creation must be visible through GET")
        before = self.snapshot()
        invalids = [
            ("missing field", {"name": marker, "status": self.sample["status"]}),
            ("unknown field", {**self.sample, "extra": "no"}),
            ("client ID", {**self.sample, "id": 7}),
            ("wrong type", {**self.sample, "name": 7}),
            ("blank name", {**self.sample, "name": "  "}),
            ("blank category", {**self.sample, "category": "  "}),
            ("unknown status", {**self.sample, "status": "not-a-status"}),
        ]
        for label, body in invalids:
            self.error(self.call("POST", "/items", body), 400, label)
            self.require(self.snapshot() == before, f"Rejected {label} changed state")
        self.error(self.call("POST", "/items", raw=b"{bad"), 400, "Malformed JSON")
        self.error(self.call("POST", "/items", raw=b"[]"), 400, "Non-object JSON")
        self.error(self.call("POST", "/items", raw=b"hello", content_type="text/plain"), 415, "Wrong media type")
        self.require(self.snapshot() == before, "Rejected JSON/media requests changed state")
        code, second, _ = self.call("POST", "/items", {**self.sample, "name": marker + " second"})
        self.require(code == 201 and isinstance(second, dict) and type(second.get("id")) is int
                     and second["id"] > item_id, "IDs must increase within this process lifetime")
        self.owned_ids.append(second["id"])

    def crud(self):
        self.create()
        item_id = self.owned_ids[0]
        replacement = {"name": "Updated check", "status": PROFILES[self.story][1], "category": "replacement"}
        code, item, _ = self.call("PUT", f"/items/{item_id}", replacement)
        self.require(code == 200 and item == {"id": item_id, **replacement}, "PUT must replace writable fields and preserve the ID")
        code, read_back, _ = self.call("GET", f"/items/{item_id}")
        self.require(code == 200 and read_back == item, "GET must show the replacement")
        before = self.snapshot()
        self.error(self.call("PUT", f"/items/{item_id}", {"name": "Partial"}), 400, "Incomplete replacement")
        self.require(self.snapshot() == before, "Rejected replacement changed state")
        code, _, raw = self.call("DELETE", f"/items/{item_id}")
        self.require(code == 204 and raw == b"", "DELETE must return 204 with an empty body")
        self.owned_ids.remove(item_id)
        self.error(self.call("GET", f"/items/{item_id}"), 404, "Read after deletion")
        self.error(self.call("DELETE", f"/items/{item_id}"), 404, "Repeated deletion")
        self.error(self.call("PUT", f"/items/{item_id}", replacement), 404, "Replace absent item")

    def cleanup(self):
        for item_id in list(self.owned_ids):
            try:
                code, _, _ = self.call("DELETE", f"/items/{item_id}")
                if code in (204, 404):
                    self.owned_ids.remove(item_id)
            except CheckFailure:
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=("starter", "create", "crud"))
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    args = parser.parse_args()
    checks = Checks(args.base_url)
    try:
        checks.common()
        getattr(checks, args.stage)()
        print(f"PASS {args.stage}: {checks.passed} checks; story={checks.story}; target={checks.base_url}")
        if args.stage == "starter":
            print("The starter is running; mutation routes intentionally remain unfinished.")
        elif args.stage == "create":
            print(f"Check-created IDs retained: {checks.owned_ids}. PUT/DELETE are not tested at this stage.")
        else:
            print("CRUD checks passed. This does not test the Docker address/restart experiment or your explanation.")
        return 0
    except CheckFailure as exc:
        print(f"FAIL {args.stage}: {exc}", file=sys.stderr)
        return 1
    finally:
        if args.stage == "crud":
            checks.cleanup()
            if checks.owned_ids:
                print(f"Could not remove check-created IDs: {checks.owned_ids}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())

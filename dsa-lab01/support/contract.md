# HTTP contract and request examples

All three stories use the same interface. Only the allowed statuses differ.

| Profile | Example name / category | Allowed statuses |
|---|---|---|
| `campus` | Prepare presentation / study | `open`, `doing`, `done` |
| `greenhouse` | Basil / herb | `healthy`, `warning`, `retired` |
| `library` | Catan / strategy | `available`, `on_loan`, `maintenance` |

Library status is descriptive. This lab does not implement a reservation or loan-coordination protocol.

## Completed interface

| Request | Success | Other required behavior |
|---|---|---|
| `GET /health` | 200, identifying the service | Supplied. |
| `GET /items` | 200, JSON array | Empty array before any creation. Supplied. |
| `GET /items/{id}` | 200, item | 404 if absent. Supplied. |
| `POST /items` | 201, created item including generated ID | Invalid input rejected without changing state. |
| `PUT /items/{id}` | 200, fully replaced item, same ID | 404 if absent. Invalid input leaves the existing item unchanged. |
| `DELETE /items/{id}` | 204, empty body | 404 if absent, including a repeated deletion. |

Writable fields are exactly `name`, `status`, `category`. All three are required for POST and PUT. Trim each string; `name` and `category` must remain nonempty; `status` must be one of the selected profile's values. Reject missing fields, unknown fields, wrong types and a client-supplied `id` with 400. PUT is **replacement**, so an omitted field is not retained automatically.

Malformed JSON or a JSON value that is not an object returns 400. A non-JSON request media type returns 415. Errors use:

```json
{"error":{"code":"...","message":"..."}}
```

Use the supplied JSON/error helpers and complete the domain validation yourself. Start with an empty dictionary. IDs increase during one process lifetime; deletion does not make an ID available again during that lifetime. After process restart, memory and the ID counter start fresh.

## A small request sequence

Examples use `greenhouse` and local port 5000. Substitute your profile's status, the actual generated ID, and the address where your service is running. A file body avoids platform-specific JSON quoting.

From the project root, save `item.json` with:

```json
{"name":"Basil","status":"healthy","category":"herb"}
```

Run these individually, inspect each response, and predict the next one. On Windows replace `curl` with `curl.exe`.

```sh
curl -i -H "Content-Type: application/json" --data-binary "@item.json" http://127.0.0.1:5000/items
curl -i http://127.0.0.1:5000/items/1
```

Change the file's name to `Mint`, then perform full replacement:

```sh
curl -i -X PUT -H "Content-Type: application/json" --data-binary "@item.json" http://127.0.0.1:5000/items/1
curl -i http://127.0.0.1:5000/items/1
curl -i -X DELETE http://127.0.0.1:5000/items/1
curl -i http://127.0.0.1:5000/items/1
```

For one rejection experiment, save an invalid body with a blank name or an unsupported status. Read the collection before the rejected request and again afterward. A correct error response alone does not establish that state stayed unchanged.

## Request path

Locally: **client → 127.0.0.1:5000 → Waitress → Flask route → dictionary → response**.

In Docker: **client → host 127.0.0.1:8085 → published container port 5000 → Waitress → Flask route → dictionary → response**.

One process and one application-processing thread make this lab's memory model simple. The HTTP contract and the state observations still matter; passing a check cannot replace explaining them.

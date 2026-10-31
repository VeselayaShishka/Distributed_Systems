# My four checkpoint observations

Write your prediction **before** running the experiment. Then use the response, state or runtime evidence to correct it. A few sentences per entry are enough; do not add a screenshot dossier.

## 1 — Meet the service

**Predict:** Which process receives `GET /items`, and what will an empty service return?

**Observe:** Record the status/body of the collection and missing-item requests.

**Explain:** Trace the request from your client through Waitress to Flask. Where does this service's data live?

## 2 — Create something valid

**Predict:** What should a valid creation return? What should a rejected creation change?

**Observe:** Record one created item's ID and one rejected request. Compare the collection before and after the rejection.

**Explain:** What does the successful response promise? Which evidence shows that rejected input changed nothing?

## 3 — Follow one item

**Predict:** What should happen to its ID during replacement? What should a second deletion return?

**Observe:** Record the create → read → replace → read → delete → missing sequence. Include statuses and the significant state change.

**Explain:** How do the responses and stored state agree?

## 4 — Move and restart it

**Predict:** What will stop/start of the same container change? Which address changes when host publication moves from 8085 to 8086?

**Observe:** Record the container name, published address and an item before/after stop/start. Then test the recreated container's new host address.

**Explain:** Distinguish the running process's memory from the image and from the published port. State which resources you cleaned up.

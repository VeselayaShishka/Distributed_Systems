"""Choose the vocabulary of your project without changing the HTTP contract."""

import os

STORIES = {
    "campus": {
        "title": "Campus tasks",
        "statuses": ("open", "doing", "done"),
        "sample": {"name": "Prepare presentation", "status": "open", "category": "study"},
    },
    "greenhouse": {
        "title": "Greenhouse catalogue",
        "statuses": ("healthy", "warning", "retired"),
        "sample": {"name": "Basil", "status": "healthy", "category": "herb"},
    },
    "library": {
        "title": "Board-game library",
        "statuses": ("available", "on_loan", "maintenance"),
        "sample": {"name": "Catan", "status": "available", "category": "strategy"},
    },
}

STORY_KEY = os.environ.get("PROJECT_STORY", "greenhouse")
if STORY_KEY not in STORIES:
    raise ValueError("PROJECT_STORY must be campus, greenhouse, or library")
STORY = STORIES[STORY_KEY]

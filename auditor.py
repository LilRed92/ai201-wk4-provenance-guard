import json
import os
from config import LOG_FILE

def write_entry(entry):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok = True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def read_entries(limit=50):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    entries = [json.loads(line) for line in lines]
    return entries[-limit:]

def update_entry(content_id, updates):
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    entries = [json.loads(line) for line in lines]
    found = False
    for entry in entries:
        if entry.get("content_id") == content_id:
            entry.update(updates)
            found = True
            break
    if found:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
    return found
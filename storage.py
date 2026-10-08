import json
import os
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(_HERE, "applications.json")

def _load():
    """Read all applications from the JSON file. Returns a list."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(applications):
    """Write the full list back to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2)

def add_application(company, role, status="applied", work_arrangement="", notes=""):
    """Add one application and return it."""
    applications = _load()
    new_app = {
        "id": len(applications) + 1,
        "company": company,
        "role": role,
        "date_applied": date.today().isoformat(),
        "status": status,
        "work_arrangement": work_arrangement,
        "notes": notes,
    }
    applications.append(new_app)
    _save(applications)
    return new_app

def list_applications():
    """Return all applications."""
    return _load()

# Quick self-test: run this file directly to confirm storage works.
if __name__ == "__main__":
    print("Adding a test application...")
    add_application(
        company="DigiCert",
        role="Senior Business Transformation Architect",
        status="applied",
        work_arrangement="unspecified",
        notes="Flagged for travel clarification",
    )
    print("All applications:")
    for app in list_applications():
        print(f"  [{app['id']}] {app['company']} - {app['role']} ({app['status']})")
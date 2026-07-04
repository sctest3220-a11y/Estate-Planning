"""Minimal file-backed user store.

Stores ONLY account credentials (hashed) and terms-acknowledgment records.
It never stores estate-planning inputs (names, passport numbers, beneficiaries,
asset values) — those are processed in memory per request and never persisted.
"""

import json
import os
import threading
from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

_LOCK = threading.Lock()


def _default_path():
    # Overridable via env so the hosted deployment can point at a writable volume.
    return os.environ.get(
        "ESTATE_USER_STORE",
        os.path.join(os.path.dirname(__file__), "users.json"),
    )


def _load(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


class UserStore:
    def __init__(self, path=None):
        self.path = path or _default_path()

    def create_user(self, username, password):
        """Returns (ok, error_message)."""
        username = (username or "").strip().lower()
        if not username:
            return False, "Username is required."
        if len(password or "") < 8:
            return False, "Password must be at least 8 characters."
        with _LOCK:
            users = _load(self.path)
            if username in users:
                return False, "That username is already taken."
            users[username] = {
                "password_hash": generate_password_hash(password),
                "created_at": _now_iso(),
                "acknowledged_terms_at": None,
            }
            _save(self.path, users)
        return True, None

    def verify(self, username, password):
        username = (username or "").strip().lower()
        with _LOCK:
            users = _load(self.path)
        user = users.get(username)
        if not user or not user.get("password_hash"):
            # No password set (e.g. a Google account) — reject local login.
            return False
        return check_password_hash(user["password_hash"], password or "")

    def create_or_get_google_user(self, email):
        """Look up or create an account for a verified Google email.

        The username is the email address; no password is stored. Returns the
        username to place in the session.
        """
        username = (email or "").strip().lower()
        if not username:
            return None
        with _LOCK:
            users = _load(self.path)
            if username not in users:
                users[username] = {
                    "password_hash": None,
                    "provider": "google",
                    "created_at": _now_iso(),
                    "acknowledged_terms_at": None,
                }
                _save(self.path, users)
        return username

    def record_acknowledgment(self, username):
        username = (username or "").strip().lower()
        with _LOCK:
            users = _load(self.path)
            if username in users:
                users[username]["acknowledged_terms_at"] = _now_iso()
                _save(self.path, users)

    def has_acknowledged(self, username):
        username = (username or "").strip().lower()
        with _LOCK:
            users = _load(self.path)
        user = users.get(username)
        return bool(user and user.get("acknowledged_terms_at"))

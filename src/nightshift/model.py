"""Local model client — the ONLY network this product may touch is localhost.

Reads NIGHTSHIFT_MODEL_URL (an OpenAI-compatible local endpoint, e.g. a model
server running on the GB10). Every failure returns None so callers fall back
to deterministic behavior. The demo must never die because a model didn't load.
"""
import json
import os
import urllib.request

TIMEOUT_S = 5


class LocalModel:
    def __init__(self, url=None, model=None):
        self.url = (url or os.environ.get("NIGHTSHIFT_MODEL_URL", "")).rstrip("/")
        self.model = model or os.environ.get("NIGHTSHIFT_MODEL", "local-model")

    def available(self):
        return bool(self.url)

    def complete(self, prompt):
        """Return completion text, or None on any failure (caller falls back)."""
        if not self.url:
            return None
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }).encode()
        req = urllib.request.Request(
            self.url + "/chat/completions", data=payload,
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return None

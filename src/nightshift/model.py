"""Local model client — the ONLY network this product may touch is localhost.

Reads NIGHTSHIFT_MODEL_URL (an OpenAI-compatible local endpoint, e.g. a model
server running on the GB10). Every failure returns None so callers fall back
to deterministic behavior. The demo must never die because a model didn't load.

Env:
  NIGHTSHIFT_MODEL_URL      e.g. http://localhost:8000/v1 (unset = no model)
  NIGHTSHIFT_MODEL          served model name; unset = ask the server (/models)
  NIGHTSHIFT_MODEL_TIMEOUT  seconds per request (default 20)
"""
import json
import os
import re
import urllib.request

DEFAULT_TIMEOUT_S = 20
SYSTEM_PROMPT = ("You edit business drafts. Reply with only the finished text: "
                 "no preamble, no quotes, no notes.")
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


class LocalModel:
    def __init__(self, url=None, model=None, timeout=None):
        self.url = (url if url is not None else os.environ.get("NIGHTSHIFT_MODEL_URL", "")).rstrip("/")
        self.model = model or os.environ.get("NIGHTSHIFT_MODEL", "")
        self.timeout = float(timeout or os.environ.get("NIGHTSHIFT_MODEL_TIMEOUT", DEFAULT_TIMEOUT_S))
        self.last_error = None

    def available(self):
        return bool(self.url)

    def _get(self, path):
        with urllib.request.urlopen(self.url + path, timeout=self.timeout) as resp:
            return json.loads(resp.read())

    def model_name(self):
        """Served model id. vLLM rejects any name it isn't serving, so ask it."""
        if not self.model:
            self.model = self._get("/models")["data"][0]["id"]
        return self.model

    def complete(self, prompt):
        """Return completion text, or None on any failure (caller falls back)."""
        if not self.url:
            return None
        try:
            payload = json.dumps({
                "model": self.model_name(),
                "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                             {"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 400,
                # Qwen3.x reasoning models: skip the thinking pass for short drafts.
                "chat_template_kwargs": {"enable_thinking": False},
            }).encode()
            req = urllib.request.Request(
                self.url + "/chat/completions", data=payload,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read())
            text = _THINK.sub("", data["choices"][0]["message"].get("content") or "").strip()
            if not text:
                raise ValueError("empty completion")
            self.last_error = None
            return text
        except Exception as e:
            self.last_error = repr(e)
            return None

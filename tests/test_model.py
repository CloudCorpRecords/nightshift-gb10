import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.nightshift.model import LocalModel


class FakeVLLM(BaseHTTPRequestHandler):
    """Mimics vLLM: serves one named model and rejects any other name."""
    served = "qwen36-heretic"
    reply = "<think>hmm</think>\nPolished draft."
    require_key = None
    seen = []

    def log_message(self, *args):
        pass

    def _unauthorized(self):
        if self.require_key and self.headers.get("Authorization") != "Bearer " + self.require_key:
            self._send(401, {"error": "unauthorized"})
            return True
        return False

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self._unauthorized():
            return
        self._send(200, {"data": [{"id": self.served}]})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self._unauthorized():
            return
        FakeVLLM.seen.append(body)
        if body["model"] != self.served:
            return self._send(404, {"error": "model not found"})
        self._send(200, {"choices": [{"message": {"content": self.reply}}]})


class LocalModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), FakeVLLM)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = "http://127.0.0.1:%d/v1" % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_discovers_served_model_and_strips_thinking(self):
        model = LocalModel(url=self.url, model="")
        self.assertEqual(model.complete("polish this"), "Polished draft.")
        self.assertEqual(FakeVLLM.seen[-1]["model"], "qwen36-heretic")
        self.assertFalse(FakeVLLM.seen[-1]["chat_template_kwargs"]["enable_thinking"])

    def test_wrong_model_name_falls_back_with_reason(self):
        model = LocalModel(url=self.url, model="local-model")
        self.assertIsNone(model.complete("polish this"))
        self.assertIn("404", model.last_error)

    def test_keyed_server_needs_bearer_key(self):
        FakeVLLM.require_key = "team-key"
        try:
            self.assertEqual(LocalModel(url=self.url, model="", key="team-key").complete("x"),
                             "Polished draft.")
            keyless = LocalModel(url=self.url, model="", key="")
            self.assertIsNone(keyless.complete("x"))
            self.assertIn("401", keyless.last_error)
        finally:
            FakeVLLM.require_key = None

    def test_empty_url_means_no_model_even_if_env_set(self):
        import os
        os.environ["NIGHTSHIFT_MODEL_URL"] = self.url
        try:
            self.assertFalse(LocalModel(url="").available())
        finally:
            del os.environ["NIGHTSHIFT_MODEL_URL"]


if __name__ == "__main__":
    unittest.main()

import json
from typing import Any, Dict
from urllib import request


class ComfyClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8188"):
        self.base_url = base_url.rstrip("/")

    def submit(self, workflow: Dict[str, Any]) -> str:
        payload = json.dumps({"prompt": workflow}).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/prompt",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        prompt_id = data.get("prompt_id")
        if not prompt_id:
            raise RuntimeError("ComfyUI did not return a prompt_id.")

        print(f"ComfyUI prompt_id: {prompt_id}")
        return prompt_id

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request

from comfy_health import ComfyHealthCheck


class ComfyClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8188"):
        self.base_url = base_url.rstrip("/")
        self.health_check = ComfyHealthCheck(self.base_url)

    def render(self, workflow: Dict[str, Any]) -> str:
        self.health_check.require_ready()
        prompt_id = self.submit(workflow)
        return self.wait_for_completion(prompt_id)

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

    def wait_for_completion(
        self,
        prompt_id: str,
        timeout_seconds: int = 600,
        poll_interval: int = 2,
    ) -> str:
        deadline = time.time() + timeout_seconds

        while time.time() < deadline:
            history = self._get_history(prompt_id)
            output_path = self._find_video_path(history, prompt_id)

            if output_path:
                return output_path

            time.sleep(poll_interval)

        raise TimeoutError(f"Timed out waiting for ComfyUI prompt {prompt_id}.")

    def _get_history(self, prompt_id: str) -> Dict[str, Any]:
        with request.urlopen(
            f"{self.base_url}/history/{prompt_id}",
            timeout=30,
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    def _find_video_path(
        self,
        history: Dict[str, Any],
        prompt_id: str,
    ) -> Optional[str]:
        prompt_history = history.get(prompt_id, {})
        outputs = prompt_history.get("outputs", {})

        for node_output in outputs.values():
            video_path = self._video_path_from_output(node_output)
            if video_path:
                return video_path

        return None

    def _video_path_from_output(self, node_output: Dict[str, Any]) -> Optional[str]:
        for key in ["videos", "gifs"]:
            outputs = node_output.get(key, [])

            for output in outputs:
                filename = output.get("filename")
                if filename:
                    subfolder = output.get("subfolder", "")
                    return str(Path("output") / subfolder / filename)

        return None

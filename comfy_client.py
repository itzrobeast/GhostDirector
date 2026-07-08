import json
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request

from comfy_health import ComfyHealthCheck
from config import DEFAULT_CONFIG


class ComfyClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        request_timeout_seconds: Optional[int] = None,
        render_timeout_seconds: Optional[int] = None,
        poll_interval_seconds: Optional[int] = None,
    ):
        self.base_url = (base_url or DEFAULT_CONFIG.comfy.base_url).rstrip("/")
        self.request_timeout_seconds = (
            request_timeout_seconds
            or DEFAULT_CONFIG.comfy.request_timeout_seconds
        )
        self.render_timeout_seconds = (
            render_timeout_seconds
            or DEFAULT_CONFIG.comfy.render_timeout_seconds
        )
        self.poll_interval_seconds = (
            poll_interval_seconds
            or DEFAULT_CONFIG.comfy.poll_interval_seconds
        )
        self.health_check = ComfyHealthCheck(
            self.base_url,
            DEFAULT_CONFIG.comfy.health_timeout_seconds,
        )

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

        with request.urlopen(
            req,
            timeout=self.request_timeout_seconds,
        ) as response:
            data = json.loads(response.read().decode("utf-8"))

        prompt_id = data.get("prompt_id")
        if not prompt_id:
            raise RuntimeError("ComfyUI did not return a prompt_id.")

        print(f"ComfyUI prompt_id: {prompt_id}")
        return prompt_id

    def wait_for_completion(
        self,
        prompt_id: str,
        timeout_seconds: Optional[int] = None,
        poll_interval: Optional[int] = None,
    ) -> str:
        timeout = timeout_seconds or self.render_timeout_seconds
        interval = poll_interval or self.poll_interval_seconds
        deadline = time.time() + timeout

        while time.time() < deadline:
            history = self._get_history(prompt_id)
            output_path = self._find_video_path(history, prompt_id)

            if output_path:
                return output_path

            time.sleep(interval)

        raise TimeoutError(f"Timed out waiting for ComfyUI prompt {prompt_id}.")

    def _get_history(self, prompt_id: str) -> Dict[str, Any]:
        with request.urlopen(
            f"{self.base_url}/history/{prompt_id}",
            timeout=self.request_timeout_seconds,
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
                    return str(
                        Path(DEFAULT_CONFIG.output_dir) / subfolder / filename
                    )

        return None

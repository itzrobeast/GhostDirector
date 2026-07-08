import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from urllib import error, request


class ComfyHealthCheckError(RuntimeError):
    """Raised when ComfyUI is not ready to accept render jobs."""


@dataclass
class ComfyHealthReport:
    server_reachable: bool = False
    api_responding: bool = False
    object_info_available: bool = False
    models_available: bool = False
    diagnostics: List[str] = field(default_factory=list)

    @property
    def healthy(self) -> bool:
        return all([
            self.server_reachable,
            self.api_responding,
            self.object_info_available,
            self.models_available,
        ])

    def summary(self) -> str:
        return "; ".join(self.diagnostics)


class ComfyHealthCheck:
    """Checks whether a local ComfyUI server is ready for rendering."""

    def __init__(self, base_url: str, timeout_seconds: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def check(self) -> ComfyHealthReport:
        report = ComfyHealthReport()
        object_info = self._get_json("/object_info", report)

        if object_info is None:
            return report

        report.server_reachable = True
        report.api_responding = True
        report.object_info_available = True
        report.diagnostics.append("ComfyUI object_info endpoint responded.")
        report.models_available = self._models_available(object_info)

        if report.models_available:
            report.diagnostics.append("ComfyUI model nodes are available.")
        else:
            report.diagnostics.append(
                "ComfyUI responded, but no model loader nodes were found."
            )

        return report

    def require_ready(self) -> ComfyHealthReport:
        report = self.check()
        if not report.healthy:
            raise ComfyHealthCheckError(
                "ComfyUI is not ready for rendering: " + report.summary()
            )

        return report

    def _get_json(
        self,
        path: str,
        report: ComfyHealthReport,
    ) -> Optional[Dict]:
        url = f"{self.base_url}{path}"

        try:
            with request.urlopen(url, timeout=self.timeout_seconds) as response:
                report.server_reachable = True
                data = json.loads(response.read().decode("utf-8"))
                report.api_responding = True
                return data
        except error.URLError as exc:
            report.diagnostics.append(
                f"ComfyUI server is not reachable at {self.base_url}: {exc}"
            )
        except json.JSONDecodeError as exc:
            report.diagnostics.append(
                f"ComfyUI endpoint returned invalid JSON at {url}: {exc}"
            )

        return None

    def _models_available(self, object_info: Dict) -> bool:
        model_words = ["checkpoint", "unet", "vae", "lora", "model"]

        for node_name in object_info.keys():
            lower_name = str(node_name).lower()
            if any(word in lower_name for word in model_words):
                return True

        return False

import json
import time
from typing import Any


class StructuredLogger:
    """Writes simple JSON log events for production pipeline actions."""

    def info(self, event: str, **fields: Any) -> None:
        self._log("INFO", event, fields)

    def warning(self, event: str, **fields: Any) -> None:
        self._log("WARNING", event, fields)

    def error(self, event: str, **fields: Any) -> None:
        self._log("ERROR", event, fields)

    def _log(self, level: str, event: str, fields: dict) -> None:
        payload = {
            "level": level,
            "event": event,
            "timestamp": time.time(),
            **fields,
        }
        print(json.dumps(payload, sort_keys=True))


logger = StructuredLogger()

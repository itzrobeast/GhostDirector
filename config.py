from dataclasses import dataclass, field


@dataclass(frozen=True)
class RenderDefaults:
    width: int = 1280
    height: int = 720
    fps: int = 24
    duration: float = 5.0
    max_retries: int = 1


@dataclass(frozen=True)
class ComfyConfig:
    base_url: str = "http://127.0.0.1:8188"
    request_timeout_seconds: int = 30
    health_timeout_seconds: int = 10
    render_timeout_seconds: int = 600
    poll_interval_seconds: int = 2


@dataclass(frozen=True)
class WorkflowConfig:
    seedance_path: str = "workflows/seedance.json"


@dataclass(frozen=True)
class GhostDirectorConfig:
    output_dir: str = "output"
    render: RenderDefaults = field(default_factory=RenderDefaults)
    comfy: ComfyConfig = field(default_factory=ComfyConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)


DEFAULT_CONFIG = GhostDirectorConfig()

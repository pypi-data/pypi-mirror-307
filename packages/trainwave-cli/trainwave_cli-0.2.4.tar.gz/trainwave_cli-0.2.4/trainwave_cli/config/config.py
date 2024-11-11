from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar

import toml


@dataclass
class Config:
    endpoint: str = "https://backend.trainwave.ai"
    api_key: str = ""


class ConfigManager:
    CONFIG_DIR = Path.home() / ".config" / "trainwave"
    CONFIG_PATH = CONFIG_DIR / "config.toml"
    DEFAULT_CONF: ClassVar[dict[str, str]] = {"api_key": ""}

    def __init__(self) -> None:
        self.config = Config()
        self._ensure_config_dir()
        self.read()

    def save(self) -> None:
        if self.config is None:
            raise ValueError("Config is not initialized")
        data = asdict(self.config)
        with open(self.CONFIG_PATH, "w") as f:
            toml.dump(data, f)
        self.read()

    def delete(self) -> None:
        self.CONFIG_PATH.unlink(missing_ok=True)

    def read(self) -> None:
        if not self.CONFIG_PATH.exists():
            self._setup_config()
        with open(self.CONFIG_PATH) as f:
            data = toml.load(f)
        self.config = Config(
            **{
                k: v for k, v in data.items() if k in Config.__dataclass_fields__.keys()
            },
        )

    def _setup_config(self) -> None:
        with open(self.CONFIG_PATH, "w") as f:
            toml.dump(self.DEFAULT_CONF, f)

    def _ensure_config_dir(self) -> None:
        self.CONFIG_DIR.mkdir(exist_ok=True, parents=True)


config_manager = ConfigManager()
config = config_manager.config

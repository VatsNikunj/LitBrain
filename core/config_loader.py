import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
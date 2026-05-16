import yaml
from pathlib import Path


def load_yaml(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_table_descriptions() -> dict:
    return load_yaml("data/metadata/table_descriptions.yaml")


def load_metric_glossary() -> dict:
    return load_yaml("data/metadata/metric_glossary.yaml")
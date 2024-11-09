"""Binary matrix configs module."""

from __future__ import annotations

from pathlib import Path

import yaml  # type: ignore[import-untyped]

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


class KNNFillingConfig:
    """KNN filling configuration."""

    DEFAULT_NUMBER_OF_NEIGHBOURS = 5
    DEFAULT_THRESHOLD = 0.3

    KEY_NUMBER_OF_NEIGHBOURS = "number_of_neighbours"
    KEY_THRESHOLD = "threshold"

    DEFAULT_YAML_FILE = Path("knn_filling_config.yaml")

    @classmethod
    def default_yaml_filepath(cls, parent_dir: Path) -> Path:
        """Return the default YAML file path."""
        return parent_dir / cls.DEFAULT_YAML_FILE

    @classmethod
    def from_dir(cls, parent_dir: Path) -> KNNFillingConfig:
        """Instantiate from directory."""
        return cls.from_yaml(cls.default_yaml_filepath(parent_dir))

    @classmethod
    def from_yaml(cls, yaml_filepath: Path) -> KNNFillingConfig:
        """Instantiate from YAML."""
        with yaml_filepath.open(encoding="utf-8") as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
            return cls.from_dict(yaml_dict)

    @classmethod
    def from_dict(cls, yaml_dict: dict) -> KNNFillingConfig:
        """Instantiate from dictionary."""
        return cls(
            number_of_neighbours=yaml_dict.get(
                cls.KEY_NUMBER_OF_NEIGHBOURS,
                cls.DEFAULT_NUMBER_OF_NEIGHBOURS,
            ),
            threshold=yaml_dict.get(
                cls.KEY_THRESHOLD,
                cls.DEFAULT_THRESHOLD,
            ),
        )

    def __init__(
        self,
        number_of_neighbours: int = DEFAULT_NUMBER_OF_NEIGHBOURS,
        threshold: float = DEFAULT_THRESHOLD,
    ) -> None:
        """Initialize."""
        self.__number_of_neighbours = number_of_neighbours
        self.__threshold = threshold

    def number_of_neighbours(self) -> int:
        """Return the number of neighbours."""
        return self.__number_of_neighbours

    def threshold(self) -> float:
        """Return the threshold."""
        return self.__threshold

    def to_dict(self) -> dict:
        """Return the dictionary representation."""
        return {
            self.KEY_NUMBER_OF_NEIGHBOURS: self.__number_of_neighbours,
            self.KEY_THRESHOLD: self.__threshold,
        }

    def to_yaml(self, yaml_filepath: Path) -> None:
        """Write to YAML."""
        with yaml_filepath.open("w", encoding="utf-8") as yaml_file:
            yaml.dump(self.to_dict(), yaml_file, Dumper=Dumper, sort_keys=False)

    def to_dir(self, parent_dir: Path) -> None:
        """Write to directory."""
        self.to_yaml(self.default_yaml_filepath(parent_dir))

    def __str__(self) -> str:
        """Return the string representation."""
        return "\n".join(
            [
                f"Number of neighbours: {self.__number_of_neighbours}",
                f"Threshold: {self.__threshold} such as"
                f" [0, {self.__threshold}[ => 0, [{self.__threshold}, 1] => 1",
            ],
        )

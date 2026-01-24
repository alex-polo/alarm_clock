import logging
from typing import TYPE_CHECKING

from playsound3 import playsound

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)


class PlaysoundPlayer:
    """Playsound player."""

    def play(self, file_path: Path, repeat: int) -> None:
        """Play sound."""
        for _ in range(repeat):
            log.info("Playing sound: %s", file_path)
            playsound(file_path)

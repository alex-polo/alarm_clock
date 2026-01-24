from typing import Protocol


class ISoundPlayer(Protocol):
    """Base sound player."""

    def play(self, file_path: str, repeat: int) -> None:
        """Play sound."""
        pass

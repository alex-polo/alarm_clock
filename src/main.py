import logging
from datetime import time  # noqa: TC003
from pathlib import Path  # noqa: TC003

from apscheduler.schedulers.blocking import BlockingScheduler
from playsound3 import PlaysoundException

from src.conf.instance import APP_SETTINGS
from src.player.playsound import PlaysoundPlayer

log = logging.getLogger(__name__)


def alarm_task(
    time: time,
    sound_path: Path,
    repeat: int,
    time_telling: bool,
) -> None:
    """Alarm task."""
    log.debug("Alarm task started, time: %s, sound: %s", time, sound_path)
    try:
        playsound_player = PlaysoundPlayer()
        playsound_player.play(
            file_path=sound_path,
            repeat=repeat,
        )
    except PlaysoundException:
        log.exception('Failed to play sound "%s"', sound_path)

    if time_telling:
        ...


def check_sound_exists(sound_path: Path) -> None:
    """Check sound exists."""
    if not sound_path.exists():
        raise ValueError(f'Sounds directory: "{sound_path}" does not exist')


def start_clock() -> None:
    """Start clock."""
    scheduler = BlockingScheduler(timezone=APP_SETTINGS.settings.time_zone)
    for alarm_signal in APP_SETTINGS.alarm.signals:
        scheduler.add_job(
            alarm_task,
            "cron",
            hour=alarm_signal.time.hour,
            minute=alarm_signal.time.minute,
            args=[
                alarm_signal.time,
                alarm_signal.sound,
                alarm_signal.repeat,
                alarm_signal.time_telling,
            ],
            id=f"alarm_{alarm_signal.time}",
        )
    scheduler.start()

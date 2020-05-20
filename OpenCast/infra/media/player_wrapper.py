from threading import Lock

import psutil

import OpenCast.infra.event.player as e
import structlog
from omxplayer import keys
from OpenCast.config import config

from .error import PlayerError


# OmxPlayer documentation: https://elinux.org/Omxplayer
class PlayerWrapper:
    def __init__(self, player_factory, evt_dispatcher):
        self._logger = structlog.get_logger(__name__)
        self._player_factory = player_factory
        self._evt_dispatcher = evt_dispatcher
        self._player = None
        self._player_lock = Lock()
        self._stop_operation_id = None

    def play(self, video, volume):
        command = ["--vol", self._downscale(volume)]
        if config["player.hide_background"] is True:
            command += ["--blank"]

        if video.subtitle is not None:
            command += ["--subtitles", video.subtitle]

        def start_player():
            self._logger.debug("Opening video", video=video, opt=command)
            try:
                self._player = self._player_factory(
                    video.path,
                    command,
                    "org.mpris.MediaPlayer2.omxplayer1",
                    self._on_exit,
                )
                return True
            except SystemError:
                self._logger.error("Dbus error", error="Couldn't connect")
                # Kill instance if it is a dbus problem
                for proc in psutil.process_iter():
                    if "omxplayer" in proc.name():
                        self._logger.debug(f"Killing process", process=proc.name())
                        proc.kill()
                return False

        player_started = False
        with self._player_lock:
            for _ in range(5):
                player_started = start_player()
                if player_started:
                    break

        if not player_started:
            raise PlayerError("error starting the player")

    def stop(self, op_id):
        def impl():
            self._stop_operation_id = op_id
            self._player.stop()
            # Event is dispatched from _on_exit

        self._exec_command(impl)

    def pause(self):
        def impl():
            self._player.play_pause()

        self._exec_command(impl)

    def unpause(self):
        def impl():
            self._player.play_pause()

        self._exec_command(impl)

    def update_subtitle_state(self, state):
        def impl():
            if state is True:
                self._player.show_subtitles()
            else:
                self._player.hide_subtitles()

        self._exec_command(impl)

    def increase_subtitle_delay(self):
        def impl():
            self._player.action(keys.INCREASE_SUBTITLE_DELAY)

        self._exec_command(impl)

    def decrease_subtitle_delay(self):
        def impl():
            self._player.action(keys.DECREASE_SUBTITLE_DELAY)

        self._exec_command(impl)

    def set_volume(self, volume):
        def impl():
            self._player.set_volume(self._downscale(volume))

        self._exec_command(impl)

    def seek(self, duration):
        def impl():
            self._player.seek(duration)

        self._exec_command(impl)

    def _downscale(self, volume):
        return volume / 100

    def _exec_command(self, command):
        with self._player_lock:
            if self._player is None:
                raise PlayerError("the player is not started")
            command()

    def _dispatch(self, event):
        self._evt_dispatcher.dispatch(event)

    def _on_exit(self, player, code):
        with self._player_lock:
            evt = e.PlayerStopped(self._stop_operation_id)
            self._stop_operation_id = None
            self._player = None
        self._dispatch(evt)

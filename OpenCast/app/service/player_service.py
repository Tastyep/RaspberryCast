import logging
import uuid
from functools import partial

from OpenCast.app.command import player_commands
from OpenCast.app.error import CommandFailure
from OpenCast.config import config
from OpenCast.domain.event import player_events as model_events
from OpenCast.domain.model.player_state import PlayerState
from OpenCast.domain.model.video import Video
from OpenCast.infra.event import player_events as infra_events
from OpenCast.infra.media import subtitle

from .service import Service

sub_config = config["Subtitle"]
logger = logging.getLogger(__name__)


class PlayerService(Service):
    def __init__(self, app_facade, data_facade, io_facade, media_facade):
        super(PlayerService, self).__init__(
            app_facade, logger, self, player_commands, infra_events
        )
        self._player_repo = data_facade.player_repo()
        self._player = media_facade.player()
        self._downloader = io_facade.video_downloader()

    # Infra event handler interface implementation

    def _player_started(self, evt):
        def impl(model):
            model.play(evt.video)

        self._update(impl)

    def _player_stopped(self, evt):
        def stop_player(model):
            model.stop()

        if evt.interrupted:
            self._update(stop_player)
            return

        def next_video(model):
            model.stop()
            model.next_video()

        model = self._player_model()
        video = model.next_video()
        self._update(next_video)
        if video is not None:
            self._player.play(video, model.volume)

    def _player_paused(self, evt):
        def impl(model):
            model.pause()

        self._update(impl)

    def _player_unpaused(self, evt):
        def impl(model):
            model.unpause()

        self._update(impl)

    def _video_seeked(self, evt):
        pass

    def _subtitle_delay_updated(self, evt):
        def impl(model):
            model.subtitle_delay = model.subtitle_delay + evt.amount

        self._update(impl)

    def _volume_updated(self, evt):
        def impl(model):
            model.volume = evt.volume

        self._update(impl)

    def _subtitle_state_changed(self, evt):
        def impl(model):
            model.subtitle_state = evt.state

        self._update(impl)

    # Command handler interface implementation

    def _play_video(self, cmd):
        # TODO: move this logs in cmd dispatcher
        logger.debug("[service] stream video, URL='{}'".format(cmd.source))

        def play_video(*_):
            def play_video(video):
                model = self._player_model()
                if model.state == PlayerState.STOPPED:
                    self._player.play(video, model.volume)
                    return

                def impl(model):
                    model.queue(video, first=True)

                self._update(impl)

            video = Video(cmd.source)
            if video.from_disk():
                video.subtitle = subtitle.load_from_video(video, sub_config.language)
                play_video(video)
            else:
                self._download_video(video, play_video, first=True)

        model = self._player_model()
        if model.state != PlayerState.STOPPED:
            self._evt_dispatcher.on(model_events.PlayerStopped, play_video)
            self._player.stop()
        else:
            play_video()

    def _queue_video(self, cmd):
        logger.debug("[service] queue video, URL='{}'".format(cmd.source))
        video = Video(cmd.source)

        def queue_video(model, video):
            model.queue(video)

        def queue_local_video(model):
            video.subtitle = subtitle.load_from_video(video, sub_config.language)
            queue_video(model, video)

        if video.from_disk():
            self._update(queue_local_video)
            return

        dl_callback = partial(self._update, queue_video)
        self._download_video(video, dl_callback, first=False)

    def _stop_video(self, cmd):
        logger.debug("[service] stop current video")
        self._player.stop()

    def _toggle_video_state(self, cmd):
        player_model = self._player_model()
        if player_model.state is PlayerState.PLAYING:
            self._player.pause()
        else:
            self._player.unpause()

    def _seek_video(self, cmd):
        logger.debug("[service] seek video time, duration={}".format(cmd.duration))
        self._player.seek(cmd.duration)

    def _change_volume(self, cmd):
        logger.debug("[service] change player volume, amount: {}".format(cmd.amount))
        model = self._player_model()
        model.volume = model.volume + cmd.amount
        self._player.set_volume(model.volume)

    def _next_video(self, cmd):
        logger.debug("[service] next video")
        model = self._player_model()
        next_video = model.next_video()
        if next_video is None:
            raise CommandFailure("no next video")

        def play_next_video(*_):
            def impl(model):
                model.next_video()

            self._update(impl)
            self._player.play(next_video, model.volume)

        if model.state is not PlayerState.STOPPED:
            self._evt_dispatcher.on(model_events.PlayerStopped, play_next_video)
            self._player.stop()
        else:
            play_next_video()

    def _prev_video(self, cmd):
        logger.debug("[service] prev video")
        model = self._player_model()
        prev_video = model.prev_video()
        if prev_video is None:
            raise CommandFailure("no previous video")

        def play_prev_video(*_):
            def impl(model):
                model.prev_video()

            self._update(impl)
            self._player.play(prev_video, model.volume)

        if model.state is not PlayerState.STOPPED:
            self._evt_dispatcher.on(model_events.PlayerStopped, play_prev_video)
            self._player.stop()
        else:
            play_prev_video()

    def _toggle_subtitle(self, cmd):
        state = not self._player_model().subtitle_state
        self._player.update_subtitle_state(state)

    def _increase_subtitle_delay(self, cmd):
        self._player.increase_subtitle_delay()

    def _decrease_subtitle_delay(self, cmd):
        self._player.increase_subtitle_delay()

    # Private

    def _player_model(self):
        return self._player_repo.get_player()

    def _download_video(self, video, dl_callback, first):
        # TODO: move this logic in extractors
        if "/playlist" in video.source:
            logger.debug("[service] playlist detected, unfolding...")
            # Generate a unique ID for the playlist
            playlist_id = uuid.uuid4()
            urls = self._downloader.extract_playlist(video.source)
            videos = [Video(u, playlist_id) for u in urls]
            logger.debug("[service] playlist url unfolded to {}".format(videos))
            self._downloader.queue(videos, dl_callback, first)
        else:
            logger.debug("[service] queue single video: {}".format(video))
            self._downloader.queue([video], dl_callback, first)

    def _update(self, mutator, *args, **kwargs):
        def impl(context):
            model = self._player_model()
            mutator(model, *args, **kwargs)
            context.update(model)
            context.commit()

        self._start_transation(self._player_repo, impl)
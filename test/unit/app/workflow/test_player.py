from unittest.mock import Mock

import OpenCast.app.command.player as Cmd
import OpenCast.domain.event.player as Evt
from OpenCast.app.workflow.player import (
    QueuePlaylistWorkflow,
    QueueVideoWorkflow,
    StreamPlaylistWorkflow,
    StreamVideoWorkflow,
    Video,
    VideoWorkflow,
)
from OpenCast.domain.service.identity import IdentityService

from .util import WorkflowTestCase


class QueueVideoWorkflowTest(WorkflowTestCase):
    def setUp(self):
        super(QueueVideoWorkflowTest, self).setUp()
        self.video_repo = Mock()
        self.video_repo.exists.return_value = True

        self.player_id = IdentityService.id_player()
        self.video = Video(
            IdentityService.id_video("source"),
            "source",
            IdentityService.id_playlist("source"),
        )
        self.workflow = self.make_workflow(
            QueueVideoWorkflow, self.video_repo, self.video,
        )

    def test_initial(self):
        self.assertTrue(self.workflow.is_INITIAL())

    def test_init_to_collecting(self):
        self.expect_workflow_creation(VideoWorkflow)
        self.workflow.start()
        self.assertTrue(self.workflow.is_COLLECTING())

    def test_collecting_to_aborted(self):
        video_workflow = self.expect_workflow_creation(VideoWorkflow)
        self.workflow.to_COLLECTING()
        video_workflow.start.assert_called_once()
        self.raise_event(self.workflow, video_workflow.Aborted, video_workflow.id)
        self.assertTrue(self.workflow.is_ABORTED())

    def test_collecting_to_queueing(self):
        video_workflow = self.expect_workflow_creation(VideoWorkflow)
        self.workflow.to_COLLECTING()
        video_workflow.start.assert_called_once()
        self.raise_event(self.workflow, video_workflow.Completed, video_workflow.id)
        self.assertTrue(self.workflow.is_QUEUEING())

    def test_queueing_to_aborted(self):
        event = VideoWorkflow.Completed(self.workflow.id)
        self.workflow.to_QUEUEING(event)
        cmd = self.expect_dispatch(Cmd.QueueVideo, self.player_id, self.video.id)
        self.raise_error(self.workflow, cmd)
        self.assertTrue(self.workflow.is_ABORTED())

    def test_queueing_to_completed(self):
        event = VideoWorkflow.Completed(self.workflow.id)
        self.workflow.to_QUEUEING(event)
        cmd = self.expect_dispatch(Cmd.QueueVideo, self.player_id, self.video.id)
        self.raise_event(
            self.workflow, Evt.VideoQueued, cmd.id, self.player_id, self.video.id,
        )
        self.assertTrue(self.workflow.is_COMPLETED())


class QueuePlaylistWorkflowTest(WorkflowTestCase):
    def setUp(self):
        super(QueuePlaylistWorkflowTest, self).setUp()
        self.video_repo = Mock()
        self.video_repo.exists.return_value = True

    def make_test_workflow(self, video_count=2):
        playlist_id = IdentityService.id_playlist(f"playlist{video_count}")
        sources = [f"src{i}" for i in range(video_count)]
        videos = [
            Video(IdentityService.id_video(source), source, playlist_id)
            for source in sources
        ]
        return self.make_workflow(QueuePlaylistWorkflow, self.video_repo, videos)

    def test_initial(self):
        workflow = self.make_test_workflow()
        self.assertTrue(workflow.is_INITIAL())

    def test_init_to_queueing(self):
        workflow = self.make_test_workflow()
        self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.start()
        self.assertTrue(workflow.is_QUEUEING())

    def test_queueing_to_queueing_from_completed(self):
        workflow = self.make_test_workflow()
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Completed, workflow.id)
        self.assertTrue(workflow.is_QUEUEING())

    def test_queueing_to_queueing_from_aborted(self):
        workflow = self.make_test_workflow()
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Aborted, workflow.id)
        self.assertTrue(workflow.is_QUEUEING())

    def test_queueing_to_completed_from_completed(self):
        workflow = self.make_test_workflow(video_count=1)
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Completed, workflow.id)
        self.assertTrue(workflow.is_COMPLETED())

    def test_queueing_to_completed_from_aborted(self):
        workflow = self.make_test_workflow(video_count=1)
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Aborted, workflow.id)
        self.assertTrue(workflow.is_COMPLETED())


class StreamVideoWorkflowTest(WorkflowTestCase):
    def setUp(self):
        super(StreamVideoWorkflowTest, self).setUp()
        self.video_repo = Mock()
        self.video_repo.exists.return_value = True

        self.player_id = IdentityService.id_player()
        self.video = Video(
            IdentityService.id_video("source"),
            "source",
            IdentityService.id_playlist("source"),
        )
        self.workflow = self.make_workflow(
            StreamVideoWorkflow, self.video_repo, self.video,
        )

    def test_initial(self):
        self.assertTrue(self.workflow.is_INITIAL())

    def test_init_to_collecting(self):
        self.expect_workflow_creation(VideoWorkflow)
        self.workflow.start()
        self.assertTrue(self.workflow.is_COLLECTING())

    def test_collecting_to_aborted(self):
        video_workflow = self.expect_workflow_creation(VideoWorkflow)
        self.workflow.to_COLLECTING()
        video_workflow.start.assert_called_once()
        self.raise_event(self.workflow, video_workflow.Aborted, video_workflow.id)
        self.assertTrue(self.workflow.is_ABORTED())

    def test_collecting_to_starting(self):
        video_workflow = self.expect_workflow_creation(VideoWorkflow)
        self.workflow.to_COLLECTING()
        video_workflow.start.assert_called_once()
        self.raise_event(self.workflow, video_workflow.Completed, video_workflow.id)
        self.assertTrue(self.workflow.is_STARTING())

    def test_starting_to_aborted(self):
        event = VideoWorkflow.Completed(self.workflow.id)
        self.workflow.to_STARTING(event)
        cmd = self.expect_dispatch(Cmd.PlayVideo, self.player_id, self.video.id)
        self.raise_error(self.workflow, cmd)
        self.assertTrue(self.workflow.is_ABORTED())

    def test_queueing_to_completed(self):
        event = VideoWorkflow.Completed(self.workflow.id)
        self.workflow.to_STARTING(event)
        cmd = self.expect_dispatch(Cmd.PlayVideo, self.player_id, self.video.id)
        self.raise_event(
            self.workflow, Evt.PlayerStarted, cmd.id, self.player_id, self.video.id,
        )
        self.assertTrue(self.workflow.is_COMPLETED())


class StreamPlaylistWorkflowTest(WorkflowTestCase):
    def setUp(self):
        super(StreamPlaylistWorkflowTest, self).setUp()
        self.video_repo = Mock()
        self.video_repo.exists.return_value = True

    def make_test_workflow(self, video_count=2):
        playlist_id = IdentityService.id_playlist(f"playlist{video_count}")
        sources = [f"src{i}" for i in range(video_count)]
        videos = [
            Video(IdentityService.id_video(source), source, playlist_id)
            for source in sources
        ]
        return self.make_workflow(StreamPlaylistWorkflow, self.video_repo, videos)

    def test_initial(self):
        workflow = self.make_test_workflow()
        self.assertTrue(workflow.is_INITIAL())

    def test_init_to_playing(self):
        workflow = self.make_test_workflow()
        self.expect_workflow_creation(StreamVideoWorkflow)
        workflow.start()
        self.assertTrue(workflow.is_PLAYING())

    def test_playing_to_queueing_from_completed(self):
        workflow = self.make_test_workflow()
        play_workflow = self.expect_workflow_creation(StreamVideoWorkflow)
        workflow.to_PLAYING(None)

        self.expect_workflow_creation(QueueVideoWorkflow)
        self.raise_event(workflow, play_workflow.Completed, workflow.id)
        self.assertTrue(workflow.is_QUEUEING())

    def test_playing_to_playing_from_aborted(self):
        workflow = self.make_test_workflow()
        play_workflow = self.expect_workflow_creation(StreamVideoWorkflow)
        workflow.to_PLAYING(None)
        self.raise_event(workflow, play_workflow.Aborted, workflow.id)
        self.assertTrue(workflow.is_PLAYING())

    def test_playing_to_completed_from_completed(self):
        workflow = self.make_test_workflow(video_count=1)
        play_workflow = self.expect_workflow_creation(StreamVideoWorkflow)
        workflow.to_PLAYING(None)
        self.raise_event(workflow, play_workflow.Completed, workflow.id)
        self.assertTrue(workflow.is_COMPLETED())

    def test_playing_to_completed_from_aborted(self):
        workflow = self.make_test_workflow(video_count=1)
        play_workflow = self.expect_workflow_creation(StreamVideoWorkflow)
        workflow.to_PLAYING(None)
        self.raise_event(workflow, play_workflow.Aborted, workflow.id)
        self.assertTrue(workflow.is_COMPLETED())

    def test_queueing_to_queueing_from_completed(self):
        workflow = self.make_test_workflow()
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Completed, workflow.id)
        self.assertTrue(workflow.is_QUEUEING())

    def test_queueing_to_queueing_from_aborted(self):
        workflow = self.make_test_workflow()
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Aborted, workflow.id)
        self.assertTrue(workflow.is_QUEUEING())

    def test_queueing_to_completed_from_completed(self):
        workflow = self.make_test_workflow(video_count=1)
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Completed, workflow.id)
        self.assertTrue(workflow.is_COMPLETED())

    def test_queueing_to_completed_from_aborted(self):
        workflow = self.make_test_workflow(video_count=1)
        queue_workflow = self.expect_workflow_creation(QueueVideoWorkflow)
        workflow.to_QUEUEING(None)
        self.raise_event(workflow, queue_workflow.Aborted, workflow.id)
        self.assertTrue(workflow.is_COMPLETED())
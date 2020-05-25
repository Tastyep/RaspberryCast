from unittest.mock import Mock


class InfraFacadeMock(Mock):
    def __init__(self):
        super(InfraFacadeMock, self).__init__()
        self.io_factory = Mock()
        self.server = Mock()
        self.media_factory = Mock()

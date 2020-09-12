""" High level HTTP server """

import aiohttp_cors as cors
import structlog
from aiohttp import web


class Server:
    def __init__(self):
        self._app = web.Application()
        self._logger = structlog.get_logger(__name__)
        self._cors = cors.setup(
            self._app,
            defaults={
                "*": cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
            },
        )

    def route(self, method, route, handle):
        route = self._app.router.add_route(method, route, handle)
        self._cors.add(route)

    def run(self, host, port):
        self._logger.info("Started", host=host, port=port)

        web.run_app(self._app, host=host, port=port)

    def make_json_response(self, status, body, dumps):
        return web.json_response(body, status=status, dumps=dumps)

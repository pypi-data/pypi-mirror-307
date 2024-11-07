# -*- encoding: utf-8 -*-
from pyzrpc.logger.logger import _Logger


class Logger(_Logger):

    def logger(self, filename: str, task_id: str = None): return super().logger(filename, task_id)

    def update(self, config: dict): super().update(config)

# -*- encoding: utf-8 -*-
import os
import uuid
import logging
from logging import handlers

from pyzrpc.meta import SubjectMeta, CONFIG_ROOT_PATH_KEY


class _Logger(SubjectMeta):
    _logger = None
    _logs_path = None
    format_str = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s (%(filename)s:%(lineno)d)')

    @property
    def logs_path(self):
        return self._logs_path

    @logs_path.setter
    def logs_path(self, value):
        self._logs_path = value

    def logger(self, filename: str, task_id: str = None):
        if self._logger is None:
            self._logger = logging.getLogger(str(uuid.uuid4()))
            self._logger.setLevel(logging.INFO)

            os.makedirs(f'{self.logs_path}/{filename}', exist_ok=True)
            if task_id is None:
                _path = f'{self.logs_path}/{filename}'
            else:
                _path = f'{self.logs_path}/{filename}/{task_id}'

            th = handlers.TimedRotatingFileHandler(filename=_path, when='MIDNIGHT', backupCount=7, encoding='utf-8')
            th.suffix = "%Y-%m-%d.log"
            th.setFormatter(self.format_str)

            ch = logging.StreamHandler()
            ch.setFormatter(self.format_str)

            self._logger.addHandler(th)
            self._logger.addHandler(ch)
        return self._logger

    def update(self, config):
        self.logs_path = os.path.join(config.get(CONFIG_ROOT_PATH_KEY), 'logs')
        os.makedirs(self.logs_path, exist_ok=True)

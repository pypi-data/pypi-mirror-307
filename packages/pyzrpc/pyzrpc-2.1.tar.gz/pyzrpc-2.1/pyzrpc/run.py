# -*- encoding: utf-8 -*-

import json
import time
import base64
import subprocess
import multiprocessing

from pyzrpc.service import service_start
from pyzrpc.work import WorkStart


class _ServiceRegistry:
    _service_list = []
    _config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def service_list(self):
        return self._service_list

    def registry(self, services):
        self._service_list = services

    def _start_service(self, _service):
        bytes_to_encode = json.dumps(self.config).encode('utf-8')
        encoded_bytes = base64.b64encode(bytes_to_encode)
        encoded_string = encoded_bytes.decode('utf-8')

        _cmd = "ids=$(ps -ef | grep " + _service.__file__ + " | grep -v 'grep' | awk '{print $2}') && sudo kill -9 $ids"
        subprocess.Popen(_cmd, shell=True).wait()

        _command = 'python3 {} --config={} --path={}'.format(
            service_start.__file__, encoded_string, _service.__file__)
        process = subprocess.Popen(_command, shell=True)
        return process.pid

    def start(self):
        for _service in self.service_list:
            service_pid = self._start_service(_service)
            time.sleep(0.5)
            multiprocessing.Process(target=WorkStart().work_start, args=(_service, self.config, service_pid,)).start()

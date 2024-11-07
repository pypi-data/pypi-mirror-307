# -*- encoding: utf-8 -*-
import sys
import json
import base64
import argparse

from nameko.cli.run import run

from pyzrpc.observer import Observer
from pyzrpc.logger import Logger
from pyzrpc.utils import RpcProxy

from pyzrpc.service.service_constructor import ServiceBuild


class _ServiceStart:

    @staticmethod
    def service_start(cls_path, config):
        _observer = Observer()

        _logger = Logger()
        _rpc_proxy = RpcProxy()

        _observer.config = config
        _observer.attach(_logger)
        _observer.attach(_rpc_proxy)
        _observer.notify()

        build = ServiceBuild()
        _cls = build.build(cls_path=cls_path, rpc_proxy=_rpc_proxy, logger=_logger)

        _logger.logger(_cls.service_name).info('service running : {}'.format(_cls.name))
        run(services=[_cls], config=_rpc_proxy.rpc_config)


if __name__ == '__main__':
    import eventlet

    eventlet.monkey_patch()

    parser = argparse.ArgumentParser(description="run service script")

    parser.add_argument("--config", type=str, help="service config")
    parser.add_argument("--path", type=str, help="service path")
    args = parser.parse_args()

    encoded_string = args.config
    encoded_bytes = encoded_string.encode('utf-8')
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_string = decoded_bytes.decode('utf-8')
    configs = json.loads(decoded_string)

    sys.path.append(configs['ROOT_PATH'])

    _ServiceStart().service_start(cls_path=args.path, config=configs)

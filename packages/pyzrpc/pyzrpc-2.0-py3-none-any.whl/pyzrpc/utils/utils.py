# -*- encoding: utf-8 -*-


import pytz
import socket
import datetime

from pyzrpc.meta import CONFIG_SOCKET_BIND_IP, CONFIG_SOCKET_BIND_PORT, CONFIG_SOCKET_SHUTDOWN_SLEEP, \
    SubjectMeta, CONFIG_AMQP_URI_KEY, CONFIG_DEFAULT_TIMEZONE, CONFIG_DEFAULT_FORMAT, CONFIG_RPC_CONFIG_KEY
from pyzrpc.utils.rpc_proxy import MyClusterRpcProxy


class _Network:

    @staticmethod
    def get_ipaddr() -> str:
        socket_tools = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tools.connect((CONFIG_SOCKET_BIND_IP, CONFIG_SOCKET_BIND_PORT))
        return socket_tools.getsockname()[0]

    @staticmethod
    def is_port_open(ip_addr: str, port: int) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip_addr, int(port)))
            s.shutdown(CONFIG_SOCKET_SHUTDOWN_SLEEP)
            return False
        except IOError:
            return True


class _FormatTime:
    _timezone = CONFIG_DEFAULT_TIMEZONE
    _format = CONFIG_DEFAULT_FORMAT

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    def get_converted_time(self):
        current_time = datetime.datetime.now()
        target_timezone = pytz.timezone(self.timezone)
        converted_time = current_time.astimezone(target_timezone)
        return converted_time.strftime(self.format)


class _GetClusterRpcProxy:

    @staticmethod
    def get_cluster_rpc_proxy(config: dict):
        return MyClusterRpcProxy(config)


class _RpcProxy(SubjectMeta):
    _rpc_config = None

    @property
    def rpc_config(self):
        return self._rpc_config

    @rpc_config.setter
    def rpc_config(self, value):
        self._rpc_config = value

    def remote_call(self, service_name: str, method_name: str, **params):
        rpc_obj = _GetClusterRpcProxy.get_cluster_rpc_proxy(self.rpc_config)

        obj = getattr(rpc_obj.start(), service_name)
        func = getattr(obj, method_name)
        data = func(**params)
        return data

    def update(self, config):
        self.rpc_config = {CONFIG_AMQP_URI_KEY: config.get(CONFIG_RPC_CONFIG_KEY)}

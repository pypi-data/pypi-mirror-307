# -*- encoding: utf-8 -*-
from pyzrpc.utils.utils import _Network, _FormatTime, _RpcProxy


class Network(_Network):

    def get_ipaddr(self) -> str: return super().get_ipaddr()

    def is_port_open(self, ip_addr: str, port: int) -> bool: return super().is_port_open(ip_addr, port)


class FormatTime(_FormatTime):

    def get_converted_time(self): return super().get_converted_time()


class RpcProxy(_RpcProxy):

    def rpc_config(self): super().rpc_config()

    def remote_call(self, service_name: str, method_name: str, **params):
        return super().remote_call(service_name, method_name, **params)

    def update(self, config): super().update(config)

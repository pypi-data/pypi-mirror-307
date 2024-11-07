# -*- encoding: utf-8 -*-
import abc

from pyzrpc.service.service_start import _ServiceStart


class ServiceConstructor(abc.ABC):
    """
    RPC Metaclass Constructor
    """

    def service_name(self): ...

    def service_version(self): ...

    def service_ipaddr(self): ...

    def rpc_proxy(self): ...

    def logger(self): ...


class ServiceStart(_ServiceStart):

    def service_start(self, cls_path, config):
        super().service_start(cls_path, config)

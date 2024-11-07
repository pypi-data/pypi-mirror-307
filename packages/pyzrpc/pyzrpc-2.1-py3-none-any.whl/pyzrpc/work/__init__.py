# -*- encoding: utf-8 -*-
import abc

from pyzrpc.rabbit import RabbitMQ
from pyzrpc.work.work_start import _WorkStart


class WorkConstructor(abc.ABC):
    """
    RPC Metaclass Constructor
    """

    def work_name(self): ...

    def work_version(self): ...

    def work_ipaddr(self): ...

    @property
    def rpc_proxy(self):
        """
            self.rpc_proxy.remote_call(
                service_name: str,
                method_name: str,
                 **params
            )
        """
        return self

    @property
    def logger(self):
        """
            logging

            self.logger.info('zerorpc')

            ...
        """
        return self

    @property
    def send_message(self) -> RabbitMQ.send_message:
        return self

    @abc.abstractmethod
    def run(self, data: dict):
        """
        Record logs：
            self.logger.info('zerorpc')

        Remote Invocation
            self.rpc_proxy.remote_call(
                service_name: str,
                method_name: str,
                 **params
            )
        """


class WorkStart(_WorkStart):

    def work_start(self, service, config, service_pid): super().work_start(service, config, service_pid)

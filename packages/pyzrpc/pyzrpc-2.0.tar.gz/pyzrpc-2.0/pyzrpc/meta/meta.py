# -*- encoding: utf-8 -*-
import abc


class Meta(abc.ABC):

    @property
    @abc.abstractmethod
    def rpc_proxy(self): ...

    @property
    @abc.abstractmethod
    def logger(self): ...

    @property
    @abc.abstractmethod
    def name(self): ...


class ServiceMeta(Meta):

    @property
    @abc.abstractmethod
    def service_name(self): ...

    @property
    @abc.abstractmethod
    def service_version(self): ...

    @property
    @abc.abstractmethod
    def service_ipaddr(self): ...


class WorkMeta(Meta):

    @property
    @abc.abstractmethod
    def work_name(self): ...

    @property
    @abc.abstractmethod
    def work_version(self): ...

    @property
    @abc.abstractmethod
    def work_ipaddr(self): ...

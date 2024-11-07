# -*- encoding: utf-8 -*-

import os
import sys
import inspect
import importlib
from nameko.rpc import rpc

from pyzrpc.meta import ServiceMeta, CONFIG_RPC_FUNCTION_KEY, CONFIG_SELF_FUNCTION_KEY, \
    CONFIG_RPC_FUNCTION_PARAM_KEY, CONFIG_RPC_FUNCTION_DEFAULT_VALUE_KEY, \
    CONFIG_RPC_FUNCTION_NAME_KEY, CONFIG_RPC_PROXY_NAME_KEY

from pyzrpc.logger import Logger
from pyzrpc.utils import Network, FormatTime, RpcProxy


class _ServiceConstructor(ServiceMeta):
    _name = None
    _logger = None
    _rpc_proxy = None
    _service_name = None
    _service_ipaddr = None
    _service_version = None
    _functions = None

    @property
    def functions(self):
        return self._functions

    @functions.setter
    def functions(self, value):
        self._functions = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def rpc_proxy(self):
        return self._rpc_proxy

    @rpc_proxy.setter
    def rpc_proxy(self, value):
        self._rpc_proxy = value

    @property
    def service_name(self):
        return self._service_name

    @service_name.setter
    def service_name(self, value):
        self._service_name = value

    @property
    def service_ipaddr(self):
        return self._service_ipaddr

    @service_ipaddr.setter
    def service_ipaddr(self, value):
        self._service_ipaddr = value

    @property
    def service_version(self):
        return self._service_version

    @service_version.setter
    def service_version(self, value):
        self._service_version = value

    @classmethod
    def setattr(cls, key, value):
        setattr(cls, key, value)


class ServiceBuild:
    _constructor = _ServiceConstructor

    def build(self, cls_path: str, rpc_proxy: RpcProxy, logger: Logger):
        _script_path = os.path.dirname(cls_path)
        sys.path.insert(0, _script_path)

        _module_name, _file_extension = os.path.splitext(os.path.basename(cls_path))

        _module = __import__(
            _module_name, globals=globals(), locals=locals(),
            fromlist=[CONFIG_RPC_FUNCTION_KEY])

        importlib.reload(_module)

        _cls = getattr(_module, CONFIG_RPC_FUNCTION_KEY)

        __dict__ = _cls.__dict__
        __functions__ = {}

        for _function_name in __dict__:
            if _function_name.startswith('__') is False:
                _function = __dict__[_function_name]

                if type(_function) in [type(lambda: None)]:
                    _params = []
                    _function = rpc(_function)
                    signa = inspect.signature(_function)
                    for _name, _param in signa.parameters.items():
                        if _name != CONFIG_SELF_FUNCTION_KEY:
                            default_value = _param.default
                            if _param.default is inspect.Parameter.empty:
                                default_value = None

                            _params.append({
                                CONFIG_RPC_FUNCTION_PARAM_KEY: _name,
                                CONFIG_RPC_FUNCTION_DEFAULT_VALUE_KEY: default_value
                            })

                    __functions__.setdefault(_function_name, _params)
                self._constructor.setattr(_function_name, _function)

        self._constructor.service_name = __dict__.get(CONFIG_RPC_FUNCTION_NAME_KEY)
        self._constructor.name = '{}_{}'.format(CONFIG_RPC_PROXY_NAME_KEY, self._constructor.service_name)
        self._constructor.logger = logger.logger(
            filename=self._constructor.service_name, task_id=CONFIG_RPC_PROXY_NAME_KEY)

        self._constructor.service_ipaddr = Network().get_ipaddr()
        self._constructor.service_version = FormatTime().get_converted_time()
        self._constructor.rpc_proxy = rpc_proxy
        self._constructor.functions = __functions__

        return self._constructor

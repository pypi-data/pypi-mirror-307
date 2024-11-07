# -*- encoding: utf-8 -*-

import os
import sys
import time
import json
import multiprocessing

from pyzrpc.meta import CONFIG_MONGO_FIELD_NAME_KEY, CONFIG_MONGO_FIELD_SERVICE_IPADDR_KEY, \
    CONFIG_MONGO_FIELD_WORK_IPADDR_KEY, CONFIG_MONGO_FIELD_WORK_VERSION_KEY, \
    CONFIG_MONGO_FIELD_WORK_NAME_KEY, CONFIG_MONGO_FIELD_WORK_PID_KEY, \
    CONFIG_MONGO_FIELD_WORK_FUNCTIONS_KEY, CONFIG_MONGO_FIELD_WORK_RUN_PROCESS_KEY, \
    CONFIG_MONGO_FIELD_WORK_MAX_PROCESS_KEY, CONFIG_MONGO_FIELD_TASK_ID_KEY, CONFIG_MONGO_FIELD_SERVICE_NAME_KEY, \
    CONFIG_MONGO_FIELD_SERVICE_VERSION_KEY, CONFIG_MONGO_FIELD_SERVICE_PID_KEY, \
    CONFIG_MONGO_FIELD_SERVICE_FUNCTIONS_KEY, CONFIG_RPC_PROXY_NAME_KEY

from pyzrpc.observer import Observer
from pyzrpc.logger import Logger
from pyzrpc.utils import RpcProxy
from pyzrpc.rabbit import RabbitMQ
from pyzrpc.mongo import DBServices, DBTasks

from pyzrpc.work.work_constructor import WorkBuild
from pyzrpc.service.service_constructor import ServiceBuild

_MAX_CPU_COUNT = multiprocessing.cpu_count() - 3


class TaskRun:

    @staticmethod
    def run(cls_path: str, config: dict, boyd: dict):
        _observer = Observer()
        _observer.config = config

        _logger = Logger()
        _rpc_proxy = RpcProxy()
        _db_service = DBServices()
        _rabbitmq = RabbitMQ()

        _observer.attach(_logger)
        _observer.attach(_rpc_proxy)
        _observer.attach(_db_service)
        _observer.attach(_rabbitmq)
        _observer.notify()

        _build = WorkBuild()
        _cls = _build.build(
            cls_path=cls_path, rpc_proxy=_rpc_proxy, logger=_logger, rabbitmq=_rabbitmq,
            task_id=boyd.get(CONFIG_MONGO_FIELD_TASK_ID_KEY)
        )

        _db_service.push_one(
            query={
                CONFIG_MONGO_FIELD_WORK_NAME_KEY: _cls.work_name,
                CONFIG_MONGO_FIELD_WORK_IPADDR_KEY: _cls.work_ipaddr
            },
            update_data={
                CONFIG_MONGO_FIELD_WORK_RUN_PROCESS_KEY: os.getpid()
            }
        )

        try:
            _cls().run(boyd)
        except Exception as e:
            _logger.logger(_cls.work_name).error(' {} work error : {}'.format(_cls.work_name, e))

        _db_service.pull_one(
            query={
                CONFIG_MONGO_FIELD_WORK_NAME_KEY: _cls.work_name,
                CONFIG_MONGO_FIELD_WORK_IPADDR_KEY: _cls.work_ipaddr
            },
            update_data={
                CONFIG_MONGO_FIELD_WORK_RUN_PROCESS_KEY: os.getpid()
            }
        )


class MqCallback:
    _name = None
    _logger = None
    _ip_addr = None
    _db_task = None
    _db_service = None
    _rpc_proxy = None
    _cls_path = None
    _config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def cls_path(self):
        return self._cls_path

    @cls_path.setter
    def cls_path(self, value):
        self._cls_path = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def ip_addr(self):
        return self._ip_addr

    @ip_addr.setter
    def ip_addr(self, value):
        self._ip_addr = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def db_task(self):
        return self._db_task

    @db_task.setter
    def db_task(self, value):
        self._db_task = value

    @property
    def db_service(self):
        return self._db_service

    @db_service.setter
    def db_service(self, value):
        self._db_service = value

    @property
    def rpc_proxy(self):
        return self._rpc_proxy

    @rpc_proxy.setter
    def rpc_proxy(self, value):
        self._rpc_proxy = value

    def mq_callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            _body = json.loads(body.decode())
            if CONFIG_MONGO_FIELD_TASK_ID_KEY in _body:
                _id = _body[CONFIG_MONGO_FIELD_TASK_ID_KEY]
                if _id in self.db_service.distinct_field_query(CONFIG_MONGO_FIELD_TASK_ID_KEY, query={}):
                    self.logger.logger(self.name).info(
                        '{} is stop, stop data : {}'.format(_id, _body))
                else:
                    _work = self.db_service.get_all_data(
                        query={
                            CONFIG_MONGO_FIELD_WORK_NAME_KEY: self.name,
                            CONFIG_MONGO_FIELD_WORK_IPADDR_KEY: self.ip_addr
                        },
                        field={
                            '_id': 0,
                            CONFIG_MONGO_FIELD_WORK_MAX_PROCESS_KEY: 1,
                            CONFIG_MONGO_FIELD_WORK_RUN_PROCESS_KEY: 1
                        }
                    )

                    _work_max_process = _work[0].get(CONFIG_MONGO_FIELD_WORK_MAX_PROCESS_KEY)
                    _work_run_process = _work[0].get(CONFIG_MONGO_FIELD_WORK_RUN_PROCESS_KEY)

                    if len(_work_run_process) < _work_max_process and len(_work_run_process) < _MAX_CPU_COUNT:
                        multiprocessing.Process(target=TaskRun.run, args=(self.cls_path, self.config, _body,)).start()
                    else:
                        time.sleep(0.2)
                        ch.basic_publish(body=body, exchange='', routing_key=self.name)
            else:
                self.logger.logger(self.name).error(
                    '{} is not find, error data : {}'.format(CONFIG_MONGO_FIELD_TASK_ID_KEY, _body))
        except Exception as e:
            self.logger.logger(self.name).error('error : {}'.format(e))


class _WorkStart:

    @staticmethod
    def work_start(service, config, service_pid):
        sys.path.append(config['ROOT_PATH'])

        _observer = Observer()
        _observer.config = config

        _logger = Logger()
        _rabbitmq = RabbitMQ()
        _rpc_proxy = RpcProxy()

        _db_task = DBTasks()
        _db_service = DBServices()

        _observer.attach(_logger)
        _observer.attach(_rabbitmq)
        _observer.attach(_rpc_proxy)
        _observer.attach(_db_task)
        _observer.attach(_db_service)
        _observer.notify()

        _build = WorkBuild()
        _cls = _build.build(
            cls_path=service.__file__, rpc_proxy=_rpc_proxy, logger=_logger,
            rabbitmq=_rabbitmq, task_id=CONFIG_RPC_PROXY_NAME_KEY)

        _service_build = ServiceBuild()
        _service_cls = _service_build.build(cls_path=service.__file__, rpc_proxy=_rpc_proxy, logger=_logger)

        _update_data = {
            CONFIG_MONGO_FIELD_WORK_IPADDR_KEY: _cls.work_ipaddr,
            CONFIG_MONGO_FIELD_WORK_NAME_KEY: _cls.work_name,
            CONFIG_MONGO_FIELD_WORK_VERSION_KEY: _cls.work_version,
            CONFIG_MONGO_FIELD_WORK_PID_KEY: os.getpid(),
            CONFIG_MONGO_FIELD_WORK_FUNCTIONS_KEY: _cls.functions,
            CONFIG_MONGO_FIELD_WORK_RUN_PROCESS_KEY: [],
            CONFIG_MONGO_FIELD_WORK_MAX_PROCESS_KEY: 5,

            # service
            CONFIG_MONGO_FIELD_NAME_KEY: _service_cls.name,
            CONFIG_MONGO_FIELD_SERVICE_IPADDR_KEY: _service_cls.service_ipaddr,
            CONFIG_MONGO_FIELD_SERVICE_NAME_KEY: _service_cls.service_name,
            CONFIG_MONGO_FIELD_SERVICE_VERSION_KEY: _service_cls.service_version,
            CONFIG_MONGO_FIELD_SERVICE_PID_KEY: service_pid,
            CONFIG_MONGO_FIELD_SERVICE_FUNCTIONS_KEY: _service_cls.functions
        }

        _logger.logger(_cls.work_name).info('work running : {}'.format(_cls.work_name))
        _logger.logger(_cls.work_name).info('update_data : {}'.format(_update_data))

        _db_service.update_many(
            query={
                CONFIG_MONGO_FIELD_NAME_KEY: _cls.name,
                CONFIG_MONGO_FIELD_SERVICE_IPADDR_KEY: _cls.work_ipaddr
            },
            update_data=_update_data,
            upsert=True
        )

        _cls_task = MqCallback()
        _cls_task.logger = _logger
        _cls_task.db_task = _db_task
        _cls_task.name = _cls.work_name
        _cls_task.rpc_proxy = _rpc_proxy
        _cls_task.db_service = _db_service
        _cls_task.ip_addr = _cls.work_ipaddr
        _cls_task.cls_path = service.__file__
        _cls_task.config = config

        while True:
            try:
                _rabbitmq.get_message(queue=_cls.work_name, callback=_cls_task.mq_callback)
            except Exception as e:
                _logger.logger(_cls.work_name).error(' {} work error : {}'.format(_cls.work_name, e))
            time.sleep(0.5)

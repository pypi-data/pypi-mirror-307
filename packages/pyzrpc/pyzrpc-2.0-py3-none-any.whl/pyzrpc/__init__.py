# -*- encoding: utf-8 -*-
import json
import uuid

from pyzrpc.logger import Logger
from pyzrpc.utils import RpcProxy, Network
from pyzrpc.rabbit import RabbitMQ
from pyzrpc.observer import Observer
from pyzrpc.mongo import DBTasks, DBServices
from pyzrpc.cipher import Cipher

from pyzrpc.work import WorkConstructor
from pyzrpc.service import ServiceConstructor

from pyzrpc.meta import CONFIG_MONGO_FIELD_WORK_NAME_KEY, CONFIG_MONGO_FIELD_WORK_IPADDR_KEY, \
    CONFIG_MONGO_FIELD_WORK_MAX_PROCESS_KEY, CONFIG_RPC_PROXY_NAME_KEY, CONFIG_ROOT_PATH_KEY

from pyzrpc.run import _ServiceRegistry


class ServiceRegistry(_ServiceRegistry):

    def config(self): super().config()

    def registry(self, services): super().registry(services)

    def start(self): super().start()


class PyZrpc:
    """
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))

        config = {
            'MONGODB_CONFIG': 'mongodb://admin:mypasswrd@127.0.0.1:27020',
            'RABBITMQ_CONFIG': 'amqp://admin:mypasswrd@127.0.0.1:5672',
            'ROOT_PATH': current_dir
        }

        zrpc = pyzrpc(config=config)
    """

    def __init__(self, config, is_cipher=False):
        self._observer = Observer()
        self._service_registry = ServiceRegistry()

        self._logger = Logger()
        self._db_task = DBTasks()
        self._rabbitmq = RabbitMQ()
        self._rpc_proxy = RpcProxy()
        self._db_service = DBServices()

        if is_cipher is False:
            self.initialization(config)
        else:
            cipher_config = Cipher(config).cipher_rsa_dec()
            config_dict = json.loads(cipher_config)
            config_dict[CONFIG_ROOT_PATH_KEY] = config[CONFIG_ROOT_PATH_KEY]
            self.initialization(config_dict)

    def initialization(self, config: dict):
        self._service_registry.config = config
        self._observer.config = config

        self._observer.attach(self._logger)
        self._observer.attach(self._db_task)
        self._observer.attach(self._rabbitmq)
        self._observer.attach(self._rpc_proxy)
        self._observer.attach(self._db_service)
        self._observer.notify()

    def service_registry(self, services: list):
        self._service_registry.registry(services=services)

    def service_start(self):
        self._service_registry.start()

    def send_message(self, queue: str, message: dict):
        self._rabbitmq.send_message(queue, message)

    def remote_call(self, service_name: str, method_name: str, **params):
        return self._rpc_proxy.remote_call(service_name, method_name, **params)

    def proxy_call(self, service_name: str, method_name: str, **params):
        _name = '{}_{}'.format(CONFIG_RPC_PROXY_NAME_KEY, service_name)
        self._logger.logger(CONFIG_RPC_PROXY_NAME_KEY).info('proxy service : {}'.format(_name))
        return self._rpc_proxy.remote_call(_name, method_name, **params)

    def get_stop_task(self, query: dict, field: dict, limit: int, skip_no: int):
        return self._db_task.get_list(query=query, field=field, limit=limit, skip_no=skip_no)

    def get_service_list(self, query: dict, field: dict, limit: int, skip_no: int):
        return self._db_service.get_list(query=query, field=field, limit=limit, skip_no=skip_no)

    def update_work_max_process(self, work_name: str, work_ipaddr: str, work_max_process: int):
        self._db_service.update_many(
            query={
                CONFIG_MONGO_FIELD_WORK_NAME_KEY: work_name,
                CONFIG_MONGO_FIELD_WORK_IPADDR_KEY: work_ipaddr
            },
            update_data={
                CONFIG_MONGO_FIELD_WORK_MAX_PROCESS_KEY: work_max_process
            }
        )

    def logger(self):
        return self._logger.logger(CONFIG_RPC_PROXY_NAME_KEY)

    @staticmethod
    def get_ipaddr():
        return str(Network().get_ipaddr())

    @staticmethod
    def get_snowflake_id():
        return str(uuid.uuid4())

    @staticmethod
    def help():
        desc = """
        install rabbitmq
            wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -echo \
            'deb https://dl.bintray.com/rabbitmq/debian bionic main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list

            sudo apt update
            sudo apt install rabbitmq-server

        rabbitmq initialization
            sudo rabbitmqctl add_user admin mypassword
            sudo rabbitmqctl set_user_tags admin administrator
            sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
            sudo rabbitmq-plugins enable rabbitmq_management
            
        mongodb install
            docker pull mongo:latest
            
            mkdir -p /data/mongo/data  
            mkdir -p /data/mongo/logs  
            mkdir -p /data/mongo/config
        
        mongo start
            sudo docker run -dit --name mongo \
            -p 27017:27017 \
            -v /data/mongo/data:/data/db \
            -v /data/mongo/logs:/var/log/mongodb \
            -e MONGO_INITDB_ROOT_USERNAME=admin \
            -e MONGO_INITDB_ROOT_PASSWORD=123456 \
            --restart=always \
            mongo:latest
        
        create user
            sudo docker exec -it mongo mongo
            
            use admin  
            db.createUser({  
                user: "test_admin",  
                pwd: "mypassword",  
                roles: [ { role: "readWrite", db: "testdb" } ]  
            })

        """

        print(desc)
